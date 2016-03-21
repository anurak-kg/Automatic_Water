import datetime
import threading
from time import sleep

from Class import helper
from Class.FlagsDate import FlagsDay
from Module.Relay import Relay


class Timer(threading.Thread):
    SLEEP_MAIN_THREAD_SECOND = 0.1

    def __init__(self, relay_list):
        super(Timer, self).__init__()
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
