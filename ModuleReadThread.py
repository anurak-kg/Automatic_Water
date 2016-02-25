import threading
from time import sleep

import configparser

from RedisDatabase import RedisDatabase
from Module.UltraSensor import UltraSensor


class ModuleReadThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(ModuleReadThread, self).__init__(group, target, name, args, kwargs, verbose)

        print("## Start ultra sensor module")
        self.ultra_sensor = UltraSensor(echo=12, trigger=6)

    def run(self):
        # Initial Ultra Sensor

        while self.database.get_app_running():
            water_ranges = self.ultra_sensor.get_ultra_sensor_rang()
            print("Water ranges = " + str(water_ranges))
            self.database.set_water_level(water_ranges)
            print "test"
            sleep(1)
