# Forza Horizon 6 self-driving
**Status:** the code compiles and the training pipeline was run end-to-end on
synthetic data. It has **not** been run against the real game: capture, key
sending and driving quality are untested until you try them.

## The idea in one paragraph

The AI never touches the game's code. It looks at the screen (pixels in), and
presses keyboard keys (actions out). You first drive yourself while the script
records *frame + which keys you held*. A neural network then learns to predict
"what would Naman press when he sees this picture?". At play time the loop is:
grab frame -> network -> press keys. This is called **imitation learning /
behavioural cloning**.

## What I took from the GTA project, and what I changed

| Stage | Original (`original_project`) | This port | Why |
|---|---|---|---|
| Screen grab | `grabscreen.py`, win32 BitBlt, `np.fromstring` (removed in new NumPy) | `capture.py`, `dxcam` with `mss` fallback | Faster, works on current NumPy. GTA needed an 800x600 window in the top-left corner; this captures the monitor and resizes. |
| Read your keys | `getkeys.py`, GetAsyncKeyState via pywin32 | `inputs.py`, same call via `ctypes` | Same idea, one less dependency. |
| Send keys | `directkeys.py`, SendInput scancodes | `inputs.py`, same technique + **PWM steering** | DirectX games ignore normal key events, so scancodes are kept. PWM: steering 0.4 = hold A/D 40% of each 50 ms, giving smooth analog-ish steering from a keyboard. |
| Labels | one 9-way class (W,S,A,D,WA,WD,SA,SD,none) | two heads: steer (L/S/R) and throttle (brake/coast/accelerate) | Fewer things to learn; steering probabilities can be turned into a smooth value. |
| Model | hand-built Inception-v3 in TFLearn, from scratch | pretrained ResNet-18 in PyTorch | TFLearn/old TensorFlow won't run on an RTX 50-series. Pretrained features need less data. |
| Balancing | deleted extra "forward" samples | weighted sampling + left/right flip augmentation | Keeps all data; flip removes left/right bias. |
| Validation | last 50 frames of each file | last 10% of frames in time order | Neighbouring frames look identical, a random split would flatter the score. |

**Not ported:** the 2022 "reboot" (regression, NPC data collectors, custom GTA
mod, server/trainer). It depends on a game mod that exposed speed, steering and
cameras. Forza has no equivalent. The closest thing is Forza's *Data Out*
telemetry (below), which this port can use optionally.

## One-time setup (Windows)

1. Python 3.10-3.12 (conda is fine): `conda create -n forza python=3.11 && conda activate forza`
2. `pip install -r requirements.txt`
3. PyTorch for your **RTX 5070 Ti** (Blackwell). I believe this needs a CUDA 12.8+ build:
   `pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128`
   Verify: `python -c "import torch;print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"`
   must print `True` and your GPU. If it prints `False`, training falls back to CPU (very slow).
4. In FH6 use **borderless/windowed-fullscreen**, and in Windows Settings > System > Display >
   Graphics set FH6 to "High performance" (the NVIDIA GPU). Confirm keyboard bindings are
   W accelerate, S brake, A/D steer, or edit `config.py`.
5. Your laptop has an Intel iGPU and an NVIDIA GPU. If `capture.py` prints "falling back to mss"
   or frames look black, that is the hybrid-GPU issue: try `DXCAM_DEVICE_IDX/OUTPUT_IDX` in `config.py`,
   or just keep mss (slower but works).

## Run order

```
python collect_data.py   # F9 start/pause, F10 save & quit. Drive 1-3 hours cleanly.
python train.py          # writes models/best.pt
python play.py           # F8 = hand control to AI, F10 = quit
```

## Optional: telemetry (Data Out)

Forza can send live car data (speed etc.) as UDP packets to your own PC. In the game look for
**Settings > HUD and Gameplay > Data Out**, turn it on, IP `127.0.0.1`, port `5300` (names may
differ in FH6; I could not confirm FH6 has it). Then run `python test_telemetry.py` while driving.
If the printed speed is believable, set `TELEMETRY_ENABLED = True` in `config.py`. Benefits: the
recorder skips menus and parked frames, and speed becomes a model input. Note the packet layout in
`telemetry.py` is the FH4/FH5 one and is unverified for FH6.

## Honest limits

* Behavioural cloning drifts: once it makes a small error it sees situations you never recorded.
  Expect it to follow a road, not race. Record recoveries and more varied roads to improve this.
* Keyboard-only data is coarse (steer is left/straight/right). PWM smooths the *output*, not the training data.
* Use single-player free roam only. Do not use this in online modes.
* A downloaded, non-Steam/Xbox copy of a game may not be a legitimate copy, and such copies can
  carry malware or lack features such as telemetry. I can't help with cracks or bypasses.
