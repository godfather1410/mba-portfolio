"""Screen capture.

Replaces the original grabscreen.py (win32 BitBlt of the desktop, ~10-20 FPS,
uses the deprecated np.fromstring). dxcam uses the Desktop Duplication API and
is much faster; mss is a slower but very compatible fallback.
"""
import cv2
import numpy as np

import config


class Capture:
    def __init__(self):
        self.backend = None
        self._cam = None
        self._mss = None
        try:
            import dxcam
            self._cam = dxcam.create(device_idx=config.DXCAM_DEVICE_IDX,
                                     output_idx=config.DXCAM_OUTPUT_IDX,
                                     output_color="RGB")
            probe = self._cam.grab(region=config.REGION)
            if probe is None:  # dxcam returns None if nothing changed yet
                probe = self._cam.grab(region=config.REGION)
            if probe is None or probe.max() == 0:
                raise RuntimeError("dxcam gave an empty/black frame")
            self.backend = "dxcam"
        except Exception as e:  # noqa: BLE001 - we really do want any failure here
            print(f"[capture] dxcam unavailable ({e}); falling back to mss")
            import mss
            self._cam = None
            self._mss = mss.mss()
            self.backend = "mss"
        print(f"[capture] using {self.backend}")
        self._last = None

    def grab(self):
        """Return an RGB uint8 array of shape (IMG_H, IMG_W, 3)."""
        if self.backend == "dxcam":
            frame = self._cam.grab(region=config.REGION)
            if frame is None:          # screen unchanged since last grab
                frame = self._last
            if frame is None:
                return np.zeros((config.IMG_H, config.IMG_W, 3), np.uint8)
        else:
            if config.REGION:
                l, t, r, b = config.REGION
                mon = {"left": l, "top": t, "width": r - l, "height": b - t}
            else:
                mon = self._mss.monitors[1]
            shot = np.asarray(self._mss.grab(mon))            # BGRA
            frame = cv2.cvtColor(shot, cv2.COLOR_BGRA2RGB)
        self._last = frame
        return cv2.resize(frame, (config.IMG_W, config.IMG_H),
                          interpolation=cv2.INTER_AREA)
