import datetime

import psutil
from pymongo import MongoClient

from Class.RedisDatabase import RedisDatabase


class Statistic:
    current_status = {}

    def __init__(self):
        self.redis_database = RedisDatabase()
        self.mongo_client = MongoClient()
        self.mongo_database = self.mongo_client["smart_aqua"]
        self.stat = self.mongo_database.statistic

    def update_data(self):
        # Water Level
        self.current_status[RedisDatabase.WATER_LEVEL] = self.redis_database.get_water_level()

        # Screen Mode
        if self.redis_database.get_screen_mode() is not None:
            self.current_status[RedisDatabase.SCREEN_MODE] = self.redis_database.get_screen_mode()
        else:
            self.current_status[RedisDatabase.SCREEN_MODE] = self.redis_database.get_screen_mode()

        # Date
        self.current_status["date"] = datetime.datetime.utcnow()

        # TEMPERATURE and HUMIDITY
        self.current_status[RedisDatabase.HUMIDITY] = float(self.redis_database.get(RedisDatabase.HUMIDITY))
        self.current_status[RedisDatabase.TEMPERATURE] = float(self.redis_database.get(RedisDatabase.TEMPERATURE))

        # CPU

        self.current_status[RedisDatabase.CPU_USAGE] = psutil.cpu_percent()

    def save(self):
        self.stat.insert_one(self.current_status)
        self.current_status = {}

    def update_and_save(self):
        self.update_data()
        self.save()
