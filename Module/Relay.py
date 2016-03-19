# coding=utf-8
import RPi.GPIO as GPIO
from pymongo import MongoClient

from Class.Log import Log


class Relay:
    ACTIVATE = 1
    DEACTIVATE = 0

    def __init__(self, name, gpio, status, time):

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

    @staticmethod
    def insert_new_relay():
        mongo_client = MongoClient()
        mongo_database = mongo_client["smart_aqua"]
        relay_collection = mongo_database["relays"]
        relay_1 = {"name": u"สวิทย์ไฟฟ้า", "gpio": 10, "active": False, "timer": None, "status": False}
        relay_2 = {"name": u"สวิทย์ไฟ 2", "gpio": 12, "active": False, "timer": None, "status": False}
        relay_3 = {"name": u"สวิทย์น้ำเข้า", "gpio": 13, "active": False, "timer": None, "status": False}
        relay_4 = {"name": u"สวิทย์น้ำออก", "gpio": 14, "active": False, "timer": None, "status": False}
        relay_collection.insert_one(relay_1)
        relay_collection.insert_one(relay_2)
        relay_collection.insert_one(relay_3)
        relay_collection.insert_one(relay_4)
