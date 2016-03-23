import datetime
from pymongo import MongoClient


class Log:
    ERROR = "ERROR"
    DEBUG = "DEBUG"

    def __init__(self):
        pass

    @staticmethod
    def new(type_error, description):
        try:
            description = description.encode('utf-8')
            mongo_client = MongoClient()
            mongo_database = mongo_client["smart_aqua"]
            log = mongo_database.logs
            log_data = {
                "type": type_error,
                "description": description,
                "date": datetime.datetime.utcnow()
            }
            log.insert_one(log_data)
            print("Log: " + str(description))

        except Exception, e:
            print(e)
            print("Error save logs")

    @staticmethod
    def debug(description):
        Log.insert(Log.DEBUG, description)

    @staticmethod
    def insert(type_error, description):
        try:
            description = description.encode('utf-8')
            mongo_client = MongoClient()
            mongo_database = mongo_client["smart_aqua"]
            log = mongo_database.logs
            log_data = {
                "type": type_error,
                "description": description,
                "date": datetime.datetime.utcnow()
            }
            log.insert_one(log_data)
            print("Log: " + str(description))

        except Exception, e:
            print(e)
            print("Error save logs")
