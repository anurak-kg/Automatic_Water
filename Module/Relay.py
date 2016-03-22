# coding=utf-8
import RPi.GPIO as GPIO
import datetime
from pymongo import MongoClient

from Class import helper
from Class.Log import Log
from Class.TimeOnOff import TimeOnOff


class Relay:
    ACTIVATE = 1
    DEACTIVATE = 0
    TYPE_SWITCH = "switch"
    TYPE_TIMER = "timer"
    TYPE_WATER_CHANGE = "water_change"

    def __init__(self, name, gpio, status, time=None, relay_type=None, active=None, object_id=None):

        self.object_id = object_id
        self.relay_type = relay_type
        self.active = active
        self.name = name
        self.time = time
        self.status = status
        self.gpio = gpio
        GPIO.setmode(GPIO.BCM)

        if gpio is not None:
            GPIO.setup(gpio, GPIO.OUT)

    def turn_on(self):
        if self.gpio is None:
            print("Error can't not found GPIO")
        else:
            GPIO.output(self.gpio, GPIO.HIGH)
            Log.new(Log.DEBUG, "Turn On! at gpio = " + str(self.gpio))

    def turn_off(self):
        if self.gpio is None:
            print("Error can't not found GPIO")
        else:
            GPIO.output(self.gpio, GPIO.LOW)
            Log.new(Log.DEBUG, "Turn Off! at gpio = " + str(self.gpio))

    def get_state(self):
        return GPIO.input(self.gpio)

    @staticmethod
    def clear_relay():
        Log.new(Log.DEBUG, "Clear relay!")
        for relay in Relay.get_relay_object_list():
            relay.turn_off()
        GPIO.cleanup()

    def get_dict(self):
        timers = []
        if self.time is None:
            timers = None
        else:
            for timer in self.time:
                timers.append(timer.get_data_dict())
        return {"name": self.name, "gpio": self.gpio, "active": self.active, "timer": timers,
                "status": self.status, "relay_type": self.relay_type}

    @staticmethod
    def get_relay_list():
        database = helper.get_database_mongo()
        return database.relays.find()

    @staticmethod
    def get_relay_object_list():

        relay_list = []
        database = helper.get_database_mongo()
        relays = database.relays.find()

        for relay_item in relays:
            relay = Relay(gpio=relay_item["gpio"], relay_type=relay_item["relay_type"], name=relay_item["name"],
                          status=relay_item["status"], time=relay_item["timer"], active=relay_item["active"],
                          object_id=relay_item["_id"])
            relay_list.append(relay)

        return relay_list

    @staticmethod
    def insert_new_relay():
        mongo_client = MongoClient()
        mongo_database = mongo_client["smart_aqua"]
        relay_collection = mongo_database["relays"]
        relay_collection.remove()
        relay1 = Relay(name=u"สวิทย์ไฟ 1",
                       gpio=26,
                       status=Relay.ACTIVATE,
                       relay_type=Relay.TYPE_SWITCH)

        relay2 = Relay(name=u"Auto 2",
                       gpio=20,
                       relay_type=Relay.TYPE_TIMER,
                       status=Relay.ACTIVATE,
                       time=[TimeOnOff(127, datetime.time(3, 0, 0), datetime.time(3, 0, 0))])

        relay3 = Relay(name=u"น้ำเข้า",
                       gpio=16,
                       relay_type=Relay.TYPE_WATER_CHANGE,
                       status=Relay.ACTIVATE)

        relay4 = Relay(name=u"น้ำออก",
                       gpio=19,
                       relay_type=Relay.TYPE_WATER_CHANGE,
                       status=Relay.ACTIVATE)

        relay_collection.insert_one(relay1.get_dict())
        relay_collection.insert_one(relay2.get_dict())
        relay_collection.insert_one(relay3.get_dict())
        relay_collection.insert_one(relay4.get_dict())
