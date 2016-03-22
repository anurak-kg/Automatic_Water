import configparser

from Class.RedisDatabase import RedisDatabase
from Class.Timer import Timer
from Module.Relay import Relay

config = configparser.ConfigParser()
config.read("config.ini")
database = RedisDatabase()
Relay.insert_new_relay()
#timer = Timer(config=config, redis_database=database)
#timer.start()
