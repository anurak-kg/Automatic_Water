# coding=utf-8
from time import sleep
import System

__author__ = 'Anurak'
RELAY1_GPIO_LIGHT = 21
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
try:
    print "Distance : \t\t %.1f   Water Temp :\t %.1f  " % (sys.get_ultra_sensor(), sys.get_water_temp())
    Humidity, Temperature = sys.get_temp_and_human()
    print "Temperature : \t %.1f   Humidity : \t %.1f " % (Temperature, Humidity)

    sys.turn_on_relay(RELAY1_GPIO_LIGHT)
    sleep(1)
    sys.turn_off_relay(RELAY1_GPIO_LIGHT)
    sleep(1)
    sys.turn_on_relay(RELAY3_GPIO_FLOW_IN)
    sleep(1)
    sys.turn_off_relay(RELAY3_GPIO_FLOW_IN)

    sys.turn_on_relay(RELAY1_GPIO_LIGHT)
    sys.turn_on_relay(RELAY2_GPIO_FLOW_OUT)
    sys.turn_on_relay(RELAY3_GPIO_FLOW_IN)
    sys.turn_on_relay(RELAY4_GPIO_OTHER)
    sleep(10)

except KeyboardInterrupt:
    print("W: interrupt received, proceeding…")
except RuntimeWarning:
    print 'Warning was raised as an exception!'

sys.cleanup()
print("Cleanup !")
