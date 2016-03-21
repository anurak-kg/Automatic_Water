import threading

import datetime
from RPi import GPIO
from time import sleep

from dateutil import parser

from Class import helper
from Class.FlagsDate import FlagsDay
from Module.Relay import Relay


class Timer(threading.Thread):
    SLEEP_MAIN_THREAD_SECOND = 0.1

    def __init__(self, redis_database, config):
        super(Timer, self).__init__()
        self.redis_database = redis_database
        self.config = config

    def run(self):
        print("## Start timer thread!")
        while self.redis_database.get_app_running():
        # for i in range(1, 100):
            self.check()
            sleep(self.SLEEP_MAIN_THREAD_SECOND)

    def check(self):
        for relay_item in Relay.get_relay_list():
            flags = FlagsDay()

            relay = Relay(gpio=relay_item["gpio"], is_timer=relay_item["gpio"], name=relay_item["name"],
                          status=relay_item["status"], time=relay_item["timer"], active=relay_item["active"],
                          object_id=relay_item["_id"])
            if relay.status is 1:
                # get current time
                today = datetime.date.today()
                day = today.strftime("%a")

                print("Relay =" + relay_item["name"])

                if relay_item["is_timer"] is True:

                    for timer in relay_item["timer"]:
                        flags.asByte = timer["day"]

                        time_checker = getattr(flags, day) == 1 and helper.time_in_range(
                            parser.parse(timer["time_on"]).time(),
                            parser.parse(timer["time_off"]).time())
                        current_relay_state = relay.get_state()
                        print("Relay state = " + str(current_relay_state))
                        print(getattr(flags, day))
                        print time_checker

                        if time_checker:
                            if current_relay_state == 0:
                                print("Turn On")
                                relay.turn_on()
                        else:
                            if current_relay_state == 1:
                                relay.turn_off()
                                print("Turn Off")

                        sleep(1)
