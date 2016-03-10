import datetime
from pymongo import MongoClient


class Log:
    ERROR = "ERROR"
    DEBUG = "DEBUG"

    def __init__(self):
        pass

    @staticmethod
    def new(type, description):
        try:
            mongo_client = MongoClient()
            mongo_database = mongo_client["smart_aqua"]
            log = mongo_database.logs
            log_data = {
                "type": type,
                "description": description,
                "date": datetime.datetime.utcnow()
            }
            log.insert_one(log_data)
        except Exception:
            print("Error save logs")
