import threading
from time import sleep
import configparser
from Database import Database
from Module.Relay import Relay
from Module.UltraSensor import UltraSensor
from ModuleReadThread import ModuleReadThread
from ScreenModule import ScreenModule

APP_VERSION = "0.0.1 Development  "

print("####### Starting.. #######")
print("####### " + APP_VERSION + " #######")

# Initial Config file
print("## initial config parser")
config = configparser.ConfigParser()
config.read("config.ini")

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
module = ModuleReadThread(name="Module")
module.start()

print("## Start Main Thread")
database = Database()
database.set_app_running(True)

try:
    while database.set_app_running():
        sleep(3)
        print threading.enumerate()

except KeyboardInterrupt:
    database.set_app_running(False)
    print("Exiting....")
    print("Current App Status = " + database.get_app_running())
    print threading.enumerate()
    raise
