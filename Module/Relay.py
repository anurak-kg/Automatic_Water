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

    def __init__(self, name, gpio, status, time, is_timer, active=None):

        self.is_timer = is_timer
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

    def clear_relay(self):
        Log.new(Log.DEBUG, "Clear relay!")
        self.turn_off()
        GPIO.cleanup()

    def get_dict(self):
        timers = []
        for timer in self.time:
            timers.append(timer.get_data_dict())
        return {"name": self.name, "gpio": self.gpio, "active": self.active, "timer": timers,
                "status": self.status, "is_timer": self.is_timer}

    @staticmethod
    def get_relay_list():
        database = helper.get_database_mongo()

        return database.relays.find()

    @staticmethod
    def insert_new_relay():
        mongo_client = MongoClient()
        mongo_database = mongo_client["smart_aqua"]
        relay_collection = mongo_database["relays"]
        relay_collection.remove()
        relay1 = Relay(name=u"สวิทย์ไฟ 1",
                       gpio=26,
                       status=Relay.ACTIVATE,
                       is_timer=True,
                       time=[TimeOnOff(128, datetime.time(3, 0, 0), datetime.time(3, 0, 0)),
                             TimeOnOff(1, datetime.time(3, 0, 0), datetime.time(3, 0, 0))])

        relay2 = Relay(name=u"สวิทย์ไฟ 2",
                       gpio=20,
                       is_timer=True,
                       status=Relay.ACTIVATE,
                       time=[TimeOnOff(128, datetime.time(3, 0, 0), datetime.time(3, 0, 0)),
                             TimeOnOff(1, datetime.time(3, 0, 0), datetime.time(3, 0, 0))])

        relay_collection.insert_one(relay1.get_dict())
        relay_collection.insert_one(relay2.get_dict())
