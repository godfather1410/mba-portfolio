"""Keyboard reading and keyboard sending (Windows only, no pywin32 needed).

Reading : GetAsyncKeyState  (same idea as the original getkeys.py)
Sending : SendInput with hardware scancodes (same idea as the original
          directkeys.py - DirectX games ignore plain virtual-key events).
Steering: the original pressed A or D fully or not at all. Here a background
          thread "pulse-width modulates" the key, so a steer value of 0.4 means
          A/D is held for 40% of every 50 ms cycle. The car then steers smoothly
          even though you only have a keyboard.
"""
import ctypes
import threading
import time
from ctypes import wintypes

import config

_user32 = ctypes.windll.user32 if hasattr(ctypes, "windll") else None
_winmm = ctypes.windll.winmm if hasattr(ctypes, "windll") else None


def key_down(vk):
    return bool(_user32.GetAsyncKeyState(vk) & 0x8000)


def read_driving_keys():
    """-> (steer_label, throttle_label) following config's label definitions."""
    a, d = key_down(config.VK_A), key_down(config.VK_D)
    w, s = key_down(config.VK_W), key_down(config.VK_S)
    steer = 1
    if a and not d:
        steer = 0
    elif d and not a:
        steer = 2
    throttle = 1
    if w and not s:
        throttle = 2
    elif s and not w:
        throttle = 0
    return steer, throttle


# ---- SendInput plumbing ----------------------------------------------------
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", wintypes.WORD), ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD), ("time", wintypes.DWORD),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", wintypes.DWORD), ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", wintypes.LONG), ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD), ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD), ("dwExtraInfo", PUL)]


class InputUnion(ctypes.Union):
    _fields_ = [("ki", KeyBdInput), ("mi", MouseInput), ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD), ("ii", InputUnion)]


KEYEVENTF_SCANCODE, KEYEVENTF_KEYUP = 0x0008, 0x0002


def _send(scancode, up):
    extra = ctypes.c_ulong(0)
    flags = KEYEVENTF_SCANCODE | (KEYEVENTF_KEYUP if up else 0)
    ii = InputUnion()
    ii.ki = KeyBdInput(0, scancode, flags, 0, ctypes.pointer(extra))
    cmd = Input(1, ii)  # 1 = INPUT_KEYBOARD
    _user32.SendInput(1, ctypes.byref(cmd), ctypes.sizeof(cmd))


class KeyboardDriver:
    """Holds the *desired* controls; a thread turns them into key presses."""

    CYCLE = 0.05  # seconds per PWM cycle

    def __init__(self):
        self.steer = 0.0      # -1 (full left) .. +1 (full right)
        self.throttle = 0     # -1 brake, 0 coast, +1 accelerate
        self._down = set()
        self._run = True
        self.enabled = True
        if _winmm:
            _winmm.timeBeginPeriod(1)   # 1 ms timer resolution for finer PWM
        self._t = threading.Thread(target=self._loop, daemon=True)
        self._t.start()

    def _set(self, sc, want):
        if want and sc not in self._down:
            _send(sc, up=False)
            self._down.add(sc)
        elif not want and sc in self._down:
            _send(sc, up=True)
            self._down.discard(sc)

    def _loop(self):
        while self._run:
            start = time.perf_counter()
            steer, thr = (self.steer, self.throttle) if self.enabled else (0.0, 0)
            self._set(config.SC_W, thr > 0)
            self._set(config.SC_S, thr < 0)
            duty = min(1.0, abs(steer))
            sc_on = config.SC_D if steer > 0 else config.SC_A
            sc_off = config.SC_A if steer > 0 else config.SC_D
            self._set(sc_off, False)
            if duty > 0.05:
                self._set(sc_on, True)
                if duty < 0.95:
                    time.sleep(self.CYCLE * duty)
                    self._set(sc_on, False)
                    time.sleep(max(0.0, self.CYCLE - (time.perf_counter() - start)))
                else:
                    time.sleep(self.CYCLE)
            else:
                self._set(sc_on, False)
                time.sleep(self.CYCLE)
        self.release_all()

    def release_all(self):
        for sc in list(self._down):
            _send(sc, up=True)
        self._down.clear()

    def close(self):
        self._run = False
        self._t.join(timeout=1.0)
        self.release_all()
