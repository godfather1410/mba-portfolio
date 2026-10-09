"""Step 3 - let the model drive.

    python play.py

Starts with AI control OFF. Click into FH6, then press F8 to hand over control
(F8 again to take it back instantly). F10 quits and releases every key.
Keep a hand on the keyboard: this is imitation learning, it WILL make mistakes.
Use single-player free roam only.
"""
import time

import numpy as np
import torch

import config
from capture import Capture
from inputs import KeyboardDriver, key_down
from model import build_model

MEAN = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
STD = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)
STEER_GAIN = 1.4      # >1 makes the car turn a bit harder than the raw probability
SMOOTH = 0.6          # 0 = no smoothing, closer to 1 = slower, smoother steering

if config.TELEMETRY_ENABLED:
    from telemetry import Telemetry


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    ckpt = torch.load(config.MODEL_DIR / "best.pt", map_location=device)
    use_speed = ckpt["use_speed"]
    if use_speed and not config.TELEMETRY_ENABLED:
        raise SystemExit("This model was trained with speed input; set TELEMETRY_ENABLED = True.")
    net = build_model(pretrained=False, use_speed=use_speed).to(device)
    net.load_state_dict(ckpt["state"])
    net.eval()

    cap = Capture()
    tel = Telemetry() if config.TELEMETRY_ENABLED else None
    drv = KeyboardDriver()
    drv.enabled = False
    dt, steer_s, ai_on = 1.0 / config.FPS, 0.0, False
    print("AI is OFF. Focus the game, press F8 to enable, F10 to quit.")
    next_t = time.perf_counter()
    try:
        while not key_down(config.KEY_QUIT):
            if key_down(config.KEY_TOGGLE_AI):
                ai_on = not ai_on
                drv.enabled = ai_on
                print("[play] AI ON" if ai_on else "[play] AI OFF")
                time.sleep(0.4)
            now = time.perf_counter()
            if now < next_t:
                time.sleep(next_t - now)
            next_t = max(next_t + dt, time.perf_counter())
            if not ai_on:
                continue

            frame = cap.grab()
            x = torch.from_numpy(frame).permute(2, 0, 1).float().unsqueeze(0) / 255.0
            x = ((x - MEAN) / STD).to(device)
            v = torch.tensor([tel.speed if tel else 0.0], device=device)
            with torch.no_grad():
                ls, lt = net(x, v)
            ps = torch.softmax(ls, 1)[0].cpu().numpy()      # [left, straight, right]
            pt = int(lt.argmax(1))                            # 0 brake, 1 coast, 2 accel
            raw = float(ps[2] - ps[0]) * STEER_GAIN
            steer_s = SMOOTH * steer_s + (1 - SMOOTH) * float(np.clip(raw, -1, 1))
            drv.steer = steer_s
            drv.throttle = pt - 1
    finally:
        drv.close()
        if tel:
            tel.close()
        print("[play] stopped, keys released")


if __name__ == "__main__":
    main()
