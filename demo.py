import ctypes

import datetime
import os
from time import sleep

from subprocess import call

import helper
from Class.FlagsDate import FlagsDay
from Class.Log import Log
from Class.Statistic import Statistic
from Class.TimeOnOff import TimeOnOff
from Class.Timer import Timer
from Module.Relay import Relay



relay_list = [Relay(name="Relay1",
                    gpio=26,
                    status=Relay.ACTIVATE,
                    time=[TimeOnOff(127, datetime.time(1, 0, 0), datetime.time(1, 20, 0))]),
              Relay(name="Relay2",
                    gpio=11,
                    status=Relay.ACTIVATE,
                    time=[TimeOnOff(128, datetime.time(3, 0, 0), datetime.time(3, 0, 0))])
              ]

# print("logout: %i" % getattr(flags, day))
# print(type(getattr(flags, day)))
# print("ss")
initial_mongodb()
timer = Timer(relay_list=relay_list)

statistic = Statistic()
Log.new("Test")
for i in range(1, 100):
    statistic.update_and_save()
    print("Saved!")
# while True:
#     timer.check()
#     sleep(1)
