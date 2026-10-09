"""Sanity-check your recordings. Run from the forza_port folder:

    python inspect_data.py

Prints a report and writes data_preview.jpg (a contact sheet of sample frames)
next to this script. Nothing is modified or deleted.
"""
import cv2
import numpy as np

import config

STEER = ["left", "straight", "right"]
THR = ["brake", "coast", "accelerate"]


def pct(a, b):
    return 100.0 * a / b if b else 0.0


def main():
    files = sorted(config.DATA_DIR.glob("shard_*.npz"))
    if not files:
        raise SystemExit(f"No shards in {config.DATA_DIR}")
    tot = 0
    steer_c = np.zeros(3, int)
    thr_c = np.zeros(3, int)
    dup = black = changes = 0
    bright = []
    speed_nan = 0
    samples = []
    prev_label = None
    print(f"{'shard':<16}{'frames':>7}  {'L/S/R %':<16}{'brake/coast/accel %':<22}{'brightness':>10}")
    for f in files:
        z = np.load(f)
        fr, st, th, sp = z["frames"], z["steer"].astype(int), z["throttle"].astype(int), z["speed"]
        n = len(fr)
        tot += n
        sc, tc = np.bincount(st, minlength=3), np.bincount(th, minlength=3)
        steer_c += sc
        thr_c += tc
        flat = fr.reshape(n, -1)
        diff = np.abs(fr[1:].astype(np.int16) - fr[:-1].astype(np.int16)).mean(axis=(1, 2, 3))
        dup += int((diff < 0.05).sum())            # frames identical to the previous one
        m = flat.mean(axis=1)
        black += int((m < 5).sum())
        bright.append(m.mean())
        labels = st * 3 + th
        changes += int((labels[1:] != labels[:-1]).sum())
        if prev_label is not None and labels[0] != prev_label:
            changes += 1
        prev_label = labels[-1]
        speed_nan += int(np.isnan(sp).sum())
        for i in np.linspace(0, n - 1, 3).astype(int):
            samples.append((fr[i], f"{f.stem[-4:]}:{STEER[st[i]][0].upper()}{THR[th[i]][0].upper()}"))
        print(f"{f.name:<16}{n:>7}  "
              f"{sc[0] * 100 // n:>3}/{sc[1] * 100 // n:>3}/{sc[2] * 100 // n:<8}"
              f"{tc[0] * 100 // n:>3}/{tc[1] * 100 // n:>3}/{tc[2] * 100 // n:<14}{m.mean():>8.0f}")

    print("\n=== TOTAL ===")
    print(f"frames: {tot}  (~{tot / config.FPS / 60:.1f} min at {config.FPS} FPS)")
    print("steer   :", {STEER[i]: f"{steer_c[i]} ({pct(steer_c[i], tot):.0f}%)" for i in range(3)})
    print("throttle:", {THR[i]: f"{thr_c[i]} ({pct(thr_c[i], tot):.0f}%)" for i in range(3)})
    print(f"duplicate consecutive frames: {pct(dup, tot):.1f}%   black frames: {pct(black, tot):.1f}%")
    print(f"key-combo changes per second: {changes / (tot / config.FPS):.2f}")
    print(f"telemetry speed recorded: {'no' if speed_nan == tot else 'yes'}")

    print("\n=== WHAT THIS MEANS ===")
    if black:
        print("! Black frames present: capture glitched or a loading screen was recorded.")
    if pct(dup, tot) > 15:
        print("! Many identical frames: capture is slower than the recording rate, "
              "or the game was paused/menu. Lower FPS in config.py or check capture backend.")
    if pct(steer_c[1], tot) > 80:
        print("! Over 80% 'straight': too little cornering. Drive more twisty roads.")
    if min(steer_c[0], steer_c[2]) < 0.05 * tot:
        print("! Very few left or right turns: model will barely learn to steer one way.")
    if pct(thr_c[2], tot) < 40:
        print("! Little accelerating: check that W is your accelerate key in-game.")
    if pct(thr_c[0], tot) > 25:
        print("! Lots of braking/reverse: check S is brake and not reverse-heavy driving.")
    if tot < 20000:
        print(f"* {tot} frames is a pipeline test, not enough to drive well "
              "(aim for roughly 60,000-200,000, i.e. 1-3 hours).")

    cols, h, w = 3, config.IMG_H, config.IMG_W
    rows = (len(samples) + cols - 1) // cols
    sheet = np.zeros((rows * h, cols * w, 3), np.uint8)
    for k, (img, tag) in enumerate(samples):
        r, c = divmod(k, cols)
        tile = cv2.cvtColor(img, cv2.COLOR_RGB2BGR).copy()
        cv2.putText(tile, tag, (4, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
        sheet[r * h:(r + 1) * h, c * w:(c + 1) * w] = tile
    out = config.ROOT / "data_preview.jpg"
    cv2.imwrite(str(out), sheet)
    print(f"\nSaved {out}")


if __name__ == "__main__":
    main()
