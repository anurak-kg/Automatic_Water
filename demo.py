import ctypes

import datetime

from Class.FlagsDate import FlagsDay

flags = FlagsDay()
flags.asByte = 98  # ->0010

today = datetime.date.today()
day = today.strftime("%a")

print("logout: %i" % getattr(flags, day))
