"""Run this while driving in FH6 to check that Data Out works.
In game: Settings > HUD and Gameplay > Data Out = ON, IP 127.0.0.1, port 5300
(menu wording may differ in FH6). Then:  python test_telemetry.py
"""
import time

from telemetry import Telemetry

t = Telemetry()
print("Listening... drive around. Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
        print(f"packets={t.packets} len={t.last_len} race_on={t.race_on} "
              f"speed={t.speed:.1f} m/s ({t.speed * 3.6:.0f} km/h)")
except KeyboardInterrupt:
    t.close()
