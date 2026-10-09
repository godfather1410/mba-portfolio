"""Find out which keys the recorder can actually see.

    python test_keys.py

Switch to FH6, drive normally for ~10 seconds (accelerate, brake, steer both
ways), then switch back here and press Ctrl+C. It prints every key it saw held
down, with the virtual-key code, plus whether W/A/S/D were detected.
"""
import ctypes
import time

user32 = ctypes.windll.user32
seen = {}
NAMES = {0x25: "LEFT", 0x26: "UP", 0x27: "RIGHT", 0x28: "DOWN", 0x20: "SPACE",
         0x10: "SHIFT", 0x11: "CTRL", 0x0D: "ENTER", 0x1B: "ESC", 0x09: "TAB"}


def name(vk):
    if vk in NAMES:
        return NAMES[vk]
    if 0x30 <= vk <= 0x39 or 0x41 <= vk <= 0x5A:
        return chr(vk)
    return f"VK_0x{vk:02X}"


print("Watching the keyboard. Go drive in the game, then come back and press Ctrl+C.")
try:
    while True:
        for vk in range(8, 255):
            if vk in (0x01, 0x02, 0x04):          # skip mouse buttons
                continue
            if user32.GetAsyncKeyState(vk) & 0x8000:
                seen[vk] = seen.get(vk, 0) + 1
        time.sleep(0.01)
except KeyboardInterrupt:
    print("\nKeys seen held down (name, code, samples):")
    for vk, n in sorted(seen.items(), key=lambda kv: -kv[1]):
        print(f"  {name(vk):<8} 0x{vk:02X}  {n}")
    print("\nW/A/S/D detected:", {c: (ord(c) in seen) for c in "WASD"})
    if not seen:
        print("No keys detected at all. The game may be running as administrator "
              "while this terminal is not (or the reverse). Run both the same way.")
