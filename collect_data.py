"""Step 1 - record your own driving.

Run, switch to FH6, then drive with W/A/S/D. Every 1/FPS second this stores
one frame plus what your keyboard was doing. F9 pauses/resumes, F10 saves & quits.

    python collect_data.py

Tips for good data (this matters more than the model):
  * Same car, same time of day, same weather for the first dataset.
  * Drive CLEANLY. The AI copies you, including your mistakes.
  * Also record "recoveries": drift toward the edge on purpose, then steer back.
    Only the steer-back part is useful, so pause (F9) while you drift out.
  * 1-3 hours of driving is a sensible first target.
"""
import time

import numpy as np

import config
from capture import Capture
from inputs import key_down, read_driving_keys

if config.TELEMETRY_ENABLED:
    from telemetry import Telemetry


def _save(frames, steer, thr, speed, idx):
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = config.DATA_DIR / f"shard_{idx:04d}.npz"
    np.savez(path, frames=np.asarray(frames, np.uint8),
             steer=np.asarray(steer, np.int8), throttle=np.asarray(thr, np.int8),
             speed=np.asarray(speed, np.float32))
    print(f"[collect] saved {path.name} ({len(frames)} frames)")


def next_shard_index():
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    existing = sorted(config.DATA_DIR.glob("shard_*.npz"))
    return int(existing[-1].stem.split("_")[1]) + 1 if existing else 1


def main():
    cap = Capture()
    tel = Telemetry() if config.TELEMETRY_ENABLED else None
    idx = next_shard_index()
    frames, steer, thr, speed = [], [], [], []
    paused, dt = True, 1.0 / config.FPS
    print("Recording starts PAUSED. Click into the game and press F9 to start. F10 = quit.")
    next_t = time.perf_counter()
    try:
        while not key_down(config.KEY_QUIT):
            if key_down(config.KEY_PAUSE):
                paused = not paused
                print("[collect] PAUSED" if paused else "[collect] RECORDING")
                time.sleep(0.4)  # debounce
            now = time.perf_counter()
            if now < next_t:
                time.sleep(max(0.0, next_t - now))
            next_t += dt
            if paused:
                next_t = time.perf_counter() + dt
                continue

            s_lab, t_lab = read_driving_keys()
            spd = tel.speed if tel else float("nan")
            if tel and (tel.race_on == 0 or (spd < 0.5 and t_lab != 2)):
                continue  # in a menu, or sitting still without pressing W: useless
            frames.append(cap.grab())
            steer.append(s_lab)
            thr.append(t_lab)
            speed.append(spd)
            if len(frames) >= config.SHARD_SIZE:
                _save(frames, steer, thr, speed, idx)
                idx += 1
                frames, steer, thr, speed = [], [], [], []
    finally:
        if frames:
            _save(frames, steer, thr, speed, idx)
        if tel:
            tel.close()
        print("[collect] done")


if __name__ == "__main__":
    main()
