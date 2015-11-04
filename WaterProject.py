# coding=utf-8
from time import sleep
import datetime
import System
import helper

__author__ = 'Anurak'

# # # # # # # # # # # # # #
# # #     SETTING     # # #
# # # # # # # # # # # # # #

RELAY1_GPIO_LIGHT = 21
RELAY1_TIMER_START = datetime.time(3, 0, 0)
RELAY1_TIMER_END = datetime.time(4, 16, 0)

RELAY2_GPIO_FLOW_OUT = 20
RELAY3_GPIO_FLOW_IN = 26
RELAY4_GPIO_OTHER = 16
SLEEP_TIME = 1  # In Second

# # # # # # # # # # # # # #
# # #     INITIALS     # # #
# # # # # # # # # # # # # #

sys = System.SystemProject()
# sys.set_ultra_sensor(Adafruit_DHT.DHT11)
sys.set_enable_water_temp(True)
sys.setup()
sys.setup_relay([RELAY1_GPIO_LIGHT, RELAY2_GPIO_FLOW_OUT, RELAY3_GPIO_FLOW_IN, RELAY4_GPIO_OTHER])

try:
    for i in range(1, 1000):
        Humidity, Temperature = sys.get_temp_and_human()

        # # # # # # # # # # # # # #
        # # #  เวลา เปิดไฟ      # # #
        # # # # # # # # # # # # # #

        if sys.timer_check(RELAY1_TIMER_START, RELAY1_TIMER_END) and sys.relay_get_state(RELAY1_GPIO_LIGHT) == 0:
            print "Turn On Light!"
            sys.turn_on_relay(RELAY1_GPIO_LIGHT)

        elif not sys.timer_check(RELAY1_TIMER_START, RELAY1_TIMER_END) and sys.relay_get_state(RELAY1_GPIO_LIGHT) == 1:
            print "Turn Off Light Now!"
            sys.turn_off_relay(RELAY1_GPIO_LIGHT)

        helper.print_terminal(ultra_sensor=sys.get_ultra_sensor(), water_temp=sys.get_water_temp(),
                              temperature=Temperature, huminity=Humidity)
        sleep(SLEEP_TIME)

except KeyboardInterrupt:
    print("W: interrupt received, proceeding…")
except RuntimeWarning:
    print 'Warning was raised as an exception!'

sys.cleanup()
print("Cleanup !")
