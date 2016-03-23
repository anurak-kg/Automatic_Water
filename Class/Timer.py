import threading
import datetime
from time import sleep
from dateutil import parser
from Class import helper
from Class.FlagsDate import FlagsDay
from Module.Relay import Relay


class Timer(threading.Thread):
    SLEEP_MAIN_THREAD_SECOND = 0.1
    DEBUG = False

    def __init__(self, redis_database, config):
        super(Timer, self).__init__()
        self.redis_database = redis_database
        self.config = config

    def run(self):
        print("## Start timer thread!")
        while self.redis_database.get_app_running():
            # for i in range(1, 100):
            self.checker()
            sleep(self.SLEEP_MAIN_THREAD_SECOND)

    def checker(self):
        for relay_item in Relay.get_relay_list():

            relay = Relay(gpio=relay_item["gpio"], relay_type=relay_item["relay_type"], name=relay_item["name"],
                          status=relay_item["status"], time=relay_item["timer"], active=relay_item["active"],
                          force_on=relay_item["force_on"], object_id=relay_item["_id"])
            if self.DEBUG:
                print("#Relay = " + relay.name + "    #Type = " + str(relay.relay_type))

            if relay.relay_type in Relay.TYPE_TIMER:
                self.timer_checker(relay)
            elif relay.relay_type in Relay.TYPE_SWITCH:
                self.switch_checker(relay)

            sleep(1)

    def timer_checker(self, relay):
        # get current time
        flags = FlagsDay()
        today = datetime.date.today()
        day = today.strftime("%a")
        for timer in relay.time:
            flags.asByte = timer["day"]
            time_checker = getattr(flags, day) == 1 and helper.time_in_range(
                parser.parse(timer["time_on"]).time(),
                parser.parse(timer["time_off"]).time())
            current_relay_state = relay.get_state()
            if self.DEBUG:
                print("Relay state = " + str(current_relay_state))
                print(relay.name + "  checker is " + str(time_checker))
                print("State = " + str(relay.force_on) + " state = " + str(current_relay_state))

            if time_checker or relay.force_on == Relay.FORCE_ON:
                if relay.force_on == Relay.FORCE_OFF and current_relay_state == Relay.ON:
                    print("Force Off")
                    relay.turn_off()
                elif current_relay_state == Relay.OFF and not relay.force_on == Relay.FORCE_OFF:
                    relay.turn_on()

            else:
                if current_relay_state == Relay.ON:
                    relay.turn_off()

    def switch_checker(self, relay):
        current_relay_state = relay.get_state()
        if self.DEBUG:
            print("Relay state = " + str(current_relay_state))
            print("State = " + str(relay.force_on) + " state = " + str(current_relay_state))

        if relay.force_on == Relay.FORCE_ON:
            if current_relay_state == Relay.OFF:
                relay.turn_on()
        else:
            if current_relay_state == Relay.ON:
                relay.turn_off()
