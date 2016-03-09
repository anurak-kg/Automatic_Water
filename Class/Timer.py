import datetime
from time import sleep

import helper
from Class.FlagsDate import FlagsDay
from Module.Relay import Relay


class Timer:
    def __init__(self, relay_list):
        self.relay_list = relay_list

    def check(self):
        for relay in self.relay_list:
            flags = FlagsDay()
            today = datetime.date.today()
            day = today.strftime("%a")

            print("Relay =" + relay.name)

            if relay.status is Relay.ACTIVATE:
                for timer in relay.time:
                    flags.asByte = timer.day
                    print(getattr(flags, day))
                    time_checker = getattr(flags, day) == 1 and helper.time_in_range(timer.time_on, timer.time_off)
                    print("Relay state = " + str(relay.get_state()))
                    print time_checker
                    if time_checker:
                        if relay.get_state() == 0:
                            relay.turn_on()
                    else:
                        if relay.get_state() == 1:
                            relay.turn_off()

                sleep(1)
