# coding=utf-8
from time import sleep
import datetime
import System
import helper

__author__ = 'Anurak'
RELAY1_GPIO_LIGHT = 21
RELAY1_TIMER_START = datetime.time(3, 0, 0)
RELAY1_TIMER_END = datetime.time(4, 13, 0)

RELAY2_GPIO_FLOW_OUT = 20
RELAY3_GPIO_FLOW_IN = 26
RELAY4_GPIO_OTHER = 16

sys = System.SystemProject()
# sys.set_ultra_sensor(Adafruit_DHT.DHT11)
sys.set_enable_water_temp(True)
sys.setup()
sys.setup_relay()
sys.add_relay(RELAY1_GPIO_LIGHT)
sys.add_relay(RELAY2_GPIO_FLOW_OUT)
sys.add_relay(RELAY3_GPIO_FLOW_IN)
sys.add_relay(RELAY4_GPIO_OTHER)

print sys.relay_list
# print(sys.relay_get_index(RELAY4_GPIO_OTHER))
try:
    for i in range(1, 100):
        print(datetime.datetime.today())
        print "Distance : \t\t %.1f   Water Temp :\t %.1f  " % (sys.get_ultra_sensor(), sys.get_water_temp())
        Humidity, Temperature = sys.get_temp_and_human()
        print "Temperature : \t %.1f   Humidity : \t %.1f " % (Temperature, Humidity)

        # # # # # # # # # # # # # #
        # # #  เวลา เปิดไฟ      # # #
        # # # # # # # # # # # # # #

        print sys.relay_get_state(RELAY1_GPIO_LIGHT)
        print sys.timer_check(RELAY1_TIMER_START, RELAY1_TIMER_END)

        if sys.timer_check(RELAY1_TIMER_START, RELAY1_TIMER_END) and sys.relay_get_state(RELAY1_GPIO_LIGHT) == 0:
            print "Turn On Light!"
            sys.turn_on_relay(RELAY1_GPIO_LIGHT)

        elif not sys.timer_check(RELAY1_TIMER_START, RELAY1_TIMER_END) and sys.relay_get_state(RELAY1_GPIO_LIGHT) == 1:
            print "Turn Off Light Now!"
            sys.turn_off_relay(RELAY1_GPIO_LIGHT)

except KeyboardInterrupt:
    print("W: interrupt received, proceeding…")
except RuntimeWarning:
    print 'Warning was raised as an exception!'

sys.cleanup()
print("Cleanup !")
