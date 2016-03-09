import threading
from time import sleep

import configparser

from Class.RedisDatabase import RedisDatabase
from Module.RelayOld import Relay
from Module.UltraSensor import UltraSensor
from ScreenModule import ScreenModule

APP_VERSION = "0.0.1 Development  "

print("####### Starting.. #######")
print("####### " + APP_VERSION + " #######")

# Initial Config file
print("## initial config parser")
config = configparser.ConfigParser()
config.read("config.ini")

database = RedisDatabase()
database.set_app_running(True)

# ###########################
# ###### Initial Module #####
# ###########################

# Initial Relay
relay = Relay(gpio_relay_1=26)

# Start TFT Monitor
print("## Start monitor")

screen = ScreenModule()
screen.start()

print("## Start Module Thread")
# module = ModuleReadThread()
# module.start()

print("## Start Main Thread")
ultra_sensor = UltraSensor(echo=12, trigger=6, number_of_sample=10)
try:
    while database.get_app_running():
        global water_ranges
        water_ranges = ultra_sensor.get_perfect_rang()
        water_ranges = None
        print "Update hardware timeout!!"
        sleep(5)
        database.set_water_level(water_ranges)
        print("Water ranges = " + str(water_ranges))


except KeyboardInterrupt:
    database.set_app_running(False)
    print("Exiting....")
    print("Current App Status = " + str(database.get_app_running()))
    print threading.enumerate()
    raise
