import ctypes
import datetime

c_uint8 = ctypes.c_uint8


class FlagsDay_bits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("Sun", c_uint8, 1),  # asByte & 1
        ("Mon", c_uint8, 1),  # asByte & 2
        ("Tue", c_uint8, 1),  # asByte & 4
        ("Wen", c_uint8, 1),  # asByte & 8
        ("Thu", c_uint8, 1),  # asByte & 16
        ("Fri", c_uint8, 1),  # asByte & 32
        ("Sat", c_uint8, 1),  # asByte & 64
    ]


class FlagsDay(ctypes.Union):
    _fields_ = [
        ("b", FlagsDay_bits),
        ("asByte", c_uint8)
    ]
    _anonymous_ = "b"
