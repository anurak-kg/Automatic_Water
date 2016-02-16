import threading
from time import sleep

import configparser

from Database import Database
from Module.UltraSensor import UltraSensor


class ModuleReadThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(ModuleReadThread, self).__init__(group, target, name, args, kwargs, verbose)

    def run(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        database = Database()

        # Initial Ultra Sensor
        print("## Start ultra sensor module")
        ultra_sensor = UltraSensor(echo=config.getint("GPIO", "Ultra_echo"),
                                   trigger=config.getint("GPIO", "Ultra_trigger"))
        while database.get_app_running():
            database.set_water_level(ultra_sensor.get_ultra_sensor_rang())
            sleep(1)

