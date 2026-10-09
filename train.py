"""Step 2 - train on the recorded shards.

    python train.py                 # defaults
    python train.py --epochs 12 --batch 64 --no-pretrained

What happens:
  1. Load every data/shard_*.npz.
  2. Hold out the LAST 10% of frames (in time order) for validation. Neighbouring
     frames are almost identical, so a random split would leak and make the
     validation score look better than it is.
  3. Re-balance: most driving is "straight", so each sample is drawn with a weight
     inversely proportional to its steer class frequency (the original project
     solved the same problem by deleting surplus 'forward' frames).
  4. Augment: random horizontal flip WITH the steer label swapped, plus brightness
     jitter. Removes any left/right bias in how you drove.
  5. Train a ResNet-18 with two cross-entropy losses (steer + throttle).
"""
import argparse
import time

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler

import config
from model import build_model

MEAN = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
STD = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)


def load_shards():
    files = sorted(config.DATA_DIR.glob("shard_*.npz"))
    if not files:
        raise SystemExit(f"No shards in {config.DATA_DIR}. Run collect_data.py first.")
    fr, st, th, sp = [], [], [], []
    for f in files:
        z = np.load(f)
        fr.append(z["frames"]); st.append(z["steer"]); th.append(z["throttle"]); sp.append(z["speed"])
    return (np.concatenate(fr), np.concatenate(st).astype(np.int64),
            np.concatenate(th).astype(np.int64), np.concatenate(sp))


class Frames(Dataset):
    def __init__(self, frames, steer, thr, speed, augment):
        self.f, self.s, self.t, self.v, self.aug = frames, steer, thr, speed, augment

    def __len__(self):
        return len(self.f)

    def __getitem__(self, i):
        img = torch.from_numpy(self.f[i]).permute(2, 0, 1).float() / 255.0
        s, t = int(self.s[i]), int(self.t[i])
        if self.aug:
            if np.random.rand() < 0.5:
                img = torch.flip(img, dims=[2])
                s = 2 - s                      # left <-> right, straight stays
            img = (img * np.random.uniform(0.8, 1.2)).clamp(0, 1)
        v = 0.0 if np.isnan(self.v[i]) else float(self.v[i])
        return img, s, t, v


def run_epoch(net, loader, opt, scaler, device, train):
    net.train(train)
    ce = nn.CrossEntropyLoss()
    tot = n = cs = ct = 0
    for img, s, t, v in loader:
        img = ((img - MEAN) / STD).to(device)
        s, t, v = s.to(device), t.to(device), v.float().to(device)
        with torch.set_grad_enabled(train):
            with torch.autocast(device_type=device.type, enabled=device.type == "cuda"):
                ls, lt = net(img, v)
                loss = ce(ls, s) + ce(lt, t)
            if train:
                opt.zero_grad(set_to_none=True)
                scaler.scale(loss).backward()
                scaler.step(opt)
                scaler.update()
        b = len(s)
        tot += loss.item() * b; n += b
        cs += (ls.argmax(1) == s).sum().item(); ct += (lt.argmax(1) == t).sum().item()
    return tot / n, cs / n, ct / n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=8)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--no-pretrained", action="store_true")
    ap.add_argument("--workers", type=int, default=0)
    args = ap.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[train] device = {device}" + (f" ({torch.cuda.get_device_name(0)})" if device.type == "cuda" else ""))
    if device.type == "cpu":
        print("[train] WARNING: CUDA not available - training on CPU will be slow. "
              "RTX 50-series needs a PyTorch build for CUDA 12.8+ (see README).")

    frames, steer, thr, speed = load_shards()
    use_speed = bool(np.isfinite(speed).all())
    n = len(frames)
    cut = int(n * 0.9)
    print(f"[train] {n} frames  (train {cut} / val {n - cut})  use_speed={use_speed}")
    print("[train] steer counts L/S/R:", np.bincount(steer, minlength=3).tolist(),
          " throttle counts S/none/W:", np.bincount(thr, minlength=3).tolist())

    tr = Frames(frames[:cut], steer[:cut], thr[:cut], speed[:cut], augment=True)
    va = Frames(frames[cut:], steer[cut:], thr[cut:], speed[cut:], augment=False)
    freq = np.bincount(steer[:cut], minlength=3).astype(float).clip(min=1)
    w = (1.0 / freq)[steer[:cut]]
    sampler = WeightedRandomSampler(w, num_samples=cut, replacement=True)
    tl = DataLoader(tr, batch_size=args.batch, sampler=sampler, num_workers=args.workers)
    vl = DataLoader(va, batch_size=args.batch, num_workers=args.workers)

    net = build_model(pretrained=not args.no_pretrained, use_speed=use_speed).to(device)
    opt = torch.optim.AdamW(net.parameters(), lr=args.lr, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=args.epochs)
    scaler = torch.amp.GradScaler(enabled=device.type == "cuda")

    config.MODEL_DIR.mkdir(parents=True, exist_ok=True)
    best = float("inf")
    for ep in range(1, args.epochs + 1):
        t0 = time.time()
        trl, trs, trt = run_epoch(net, tl, opt, scaler, device, True)
        vll, vas, vat = run_epoch(net, vl, None, scaler, device, False)
        sched.step()
        print(f"epoch {ep:02d}  train loss {trl:.3f} (steer {trs:.2f} thr {trt:.2f})  "
              f"val loss {vll:.3f} (steer {vas:.2f} thr {vat:.2f})  {time.time() - t0:.0f}s")
        if vll < best:
            best = vll
            torch.save({"state": net.state_dict(), "use_speed": use_speed},
                       config.MODEL_DIR / "best.pt")
            print("   saved models/best.pt")


if __name__ == "__main__":
    main()
