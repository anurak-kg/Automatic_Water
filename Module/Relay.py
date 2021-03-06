# coding=utf-8
import RPi.GPIO as GPIO
import datetime

from bson import ObjectId
from pymongo import MongoClient

from Class import helper
from Class.Log import Log
from Class.TimeOnOff import TimeOnOff


class Relay:
    FORCE_DISABLE = 0
    ACTIVATE = 1
    DEACTIVATE = 0
    TYPE_SWITCH = "switch"
    TYPE_TIMER = "timer"
    TYPE_WATER_CHANGE = "water_change"
    FORCE_ON = 2
    FORCE_OFF = -1
    ON = 1
    OFF = 0

    def __init__(self, name, gpio, status=OFF, time=None, relay_type=None, active=None, object_id=None, force_on=None):

        self.force_on = force_on
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
            Log.new(Log.DEBUG, "Turn On!  > " + self.name + " < at gpio = " + str(self.gpio))

    def get_object_id(self):
        return str(self.object_id)

    def turn_off(self):
        if self.gpio is None:
            print("Error can't not found GPIO")
        else:
            GPIO.output(self.gpio, GPIO.LOW)
            Log.new(Log.DEBUG, "Turn Off! > " + self.name + " <   at gpio = " + str(self.gpio))

    def get_state(self):
        return GPIO.input(self.gpio)

    @staticmethod
    def clear_relay():
        Log.new(Log.DEBUG, "Clear relay!")
        for relay in Relay.get_relay_object_list():
            Relay.set_force_on(relay.get_object_id(), Relay.FORCE_DISABLE)
            relay.turn_off()
        GPIO.cleanup()

    @staticmethod
    def set_force_on(object_id, value):
        db_client = helper.get_database_mongo()
        db_client.relays.update({
            '_id': ObjectId(object_id)}, {
            '$set': {
                'force_on': value
            }}, upsert=False)
        Log.debug("Set Force on =" + str(value) + " Relay id=" + object_id)

    def get_dict(self):
        timers = []
        if self.time is None:
            timers = None
        else:
            for timer in self.time:
                timers.append(timer.get_data_dict())
        return {"name": self.name, "gpio": self.gpio, "active": self.active, "timer": timers,
                "status": self.status, "relay_type": self.relay_type, "force_on": self.force_on}

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
                          force_on=relay_item["force_on"],
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
                       active=Relay.ACTIVATE,
                       force_on=Relay.OFF,

                       relay_type=Relay.TYPE_SWITCH)

        relay2 = Relay(name=u"Auto 2",
                       gpio=20,
                       relay_type=Relay.TYPE_TIMER,
                       active=Relay.ACTIVATE,
                       force_on=Relay.OFF,
                       time=[TimeOnOff(127, datetime.time(3, 0, 0), datetime.time(4, 0, 0))])

        relay3 = Relay(name=u"น้ำเข้า",
                       gpio=16,
                       force_on=Relay.OFF,
                       relay_type=Relay.TYPE_WATER_CHANGE,
                       active=Relay.ACTIVATE)

        relay4 = Relay(name=u"น้ำออก",
                       gpio=19,
                       force_on=Relay.OFF,
                       relay_type=Relay.TYPE_WATER_CHANGE,
                       active=Relay.ACTIVATE)

        relay_collection.insert_one(relay1.get_dict())
        relay_collection.insert_one(relay2.get_dict())
        relay_collection.insert_one(relay3.get_dict())
        relay_collection.insert_one(relay4.get_dict())
