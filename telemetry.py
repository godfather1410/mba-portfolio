"""Optional reader for Forza's "Data Out" UDP stream.

Only the first fields of the packet are used, and the layout below is the one
documented for Forza Motorsport 7 / Forza Horizon 4 / 5 ("Sled" block):
    int32  IsRaceOn            @ 0
    uint32 TimestampMS         @ 4
    float  EngineMaxRpm        @ 8
    float  EngineIdleRpm       @ 12
    float  CurrentEngineRpm    @ 16
    float  AccelerationX/Y/Z   @ 20,24,28
    float  VelocityX/Y/Z       @ 32,36,40   (m/s, world space)
I could NOT verify that FH6 keeps this layout. Run test_telemetry.py while
driving: if speed looks sane (e.g. ~30 m/s at ~110 km/h) the layout holds.
"""
import socket
import struct
import threading

import config


class Telemetry:
    def __init__(self):
        self.speed = 0.0       # m/s
        self.race_on = 0
        self.packets = 0
        self.last_len = 0
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((config.TELEMETRY_HOST, config.TELEMETRY_PORT))
        self._sock.settimeout(0.5)
        self._run = True
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while self._run:
            try:
                data, _ = self._sock.recvfrom(2048)
            except socket.timeout:
                continue
            except OSError:
                return
            self.last_len = len(data)
            if len(data) < 44:
                continue
            self.race_on = struct.unpack_from("<i", data, 0)[0]
            vx, vy, vz = struct.unpack_from("<3f", data, 32)
            self.speed = (vx * vx + vy * vy + vz * vz) ** 0.5
            self.packets += 1

    def close(self):
        self._run = False
        self._sock.close()
