"""Shared settings for the Forza Horizon 6 port. Edit here, nowhere else."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"          # recorded shards (.npz) go here
MODEL_DIR = ROOT / "models"       # trained weights go here

# ---- screen capture -------------------------------------------------------
# Full-screen capture of one monitor, then resized. Run FH6 in BORDERLESS or
# fullscreen-windowed mode. If you run it in a small window, set REGION to
# (left, top, right, bottom) in screen pixels.
REGION = None
# dxcam picks (device_idx, output_idx). On a laptop whose screen is wired to the
# Intel iGPU, 0/0 is usually right. If frames come back black, change these or
# let capture.py fall back to mss.
DXCAM_DEVICE_IDX = 0
DXCAM_OUTPUT_IDX = 0

# Model input size (width, height). 16:9, small enough to train fast.
IMG_W, IMG_H = 224, 126

# ---- recording / driving loop --------------------------------------------
FPS = 20                          # frames per second for BOTH recording and playing
SHARD_SIZE = 1000                 # frames per .npz file

# Hot-keys. Chosen to not clash with Forza's default bindings (check yours).
KEY_PAUSE = 0x78    # F9  : pause / resume recording
KEY_QUIT = 0x79     # F10 : stop the script, release all keys
KEY_TOGGLE_AI = 0x77  # F8 : turn AI control on/off while play.py is running

# Forza keyboard bindings (scancodes). Defaults assumed: W accel, S brake, A/D steer.
SC_W, SC_A, SC_S, SC_D = 0x11, 0x1E, 0x1F, 0x20
# Virtual-key codes used only for READING your keyboard while recording.
VK_W, VK_A, VK_S, VK_D = 0x57, 0x41, 0x53, 0x44

# ---- labels ---------------------------------------------------------------
# Two small heads instead of the original 9-way joint class:
#   steer:    0 = left, 1 = straight, 2 = right
#   throttle: 0 = brake/reverse (S), 1 = coast (nothing), 2 = accelerate (W)
N_STEER, N_THROTTLE = 3, 3

# ---- Forza "Data Out" telemetry (optional) --------------------------------
TELEMETRY_ENABLED = False         # set True after you verified test_telemetry.py
TELEMETRY_HOST = "127.0.0.1"
TELEMETRY_PORT = 5300             # must match the port you type in the game menu
