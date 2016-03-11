# coding=utf-8
import datetime
import socket
import spidev
from time import sleep
import stopit

import RPi.GPIO as GPIO
import configparser
import traceback
from PIL import ImageFont
from subprocess import call

from Class.Log import Log
from Class.RedisDatabase import RedisDatabase
from Class.Statistic import Statistic
from Class.Timeout import TimeoutError
from DisplayScreen import DisplayScreen
from Module.UltraSensor import UltraSensor
from lib_tft24T import TFT24T

APP_VERSION = "0.0.1 Development  "


class MainApplication(object):
    def __init__(self):
        self.water_level_error_count = 0
        self.debug = True
        print("###################################")
        print("#######       Welcome       #######")
        print("####### " + APP_VERSION + " #######")
        print("###################################")

        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.init_ip()
        self.initial_display()
        self.database = RedisDatabase()
        self.pre_process()
        self.database.set_screen_mode(DisplayScreen.MAIN)

        self.initial_hardware_module()
        self.initial_mongodb()
        self.statistic = Statistic()
        self.start()

    def start(self):
        print("Start Main Thread!")
        self.database.set_app_running(True)
        while self.database.get_app_running():

            mode = self.database.get_screen_mode()
            if mode == DisplayScreen.MAIN:
                self.display_main()
            elif mode == DisplayScreen.CLEAR:
                self._display_clear()

            try:
                self.update_hardware_module()
            except Exception, e:
                print("ERROR update_hardware_module 0x00001")
                Log.new(Log.ERROR, "ERROR update_hardware_module 0x00001")
                Log.new(Log.ERROR, "" + str(e))
                traceback.print_exc()

            # #Save statistic to mongodb
            try:
                self.statistic.update_and_save()
            except Exception, e:
                print("ERROR self.statistic.update_and_save() 0x00002")
                Log.new(Log.ERROR, "ERROR self.statistic.update_and_save() 0x00002")
                Log.new(Log.ERROR, "" + str(e))

            sleep(1)
        print("Stopped!")

    def init_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com", 80))
        self.ip = s.getsockname()[0]
        s.close()

    def initial_hardware_module(self):
        self.ultra_sensor = UltraSensor(echo=12, trigger=6, number_of_sample=10)

    @staticmethod
    def initial_mongodb():
        try:
            print("Initial Mongodb")
            call("sudo rm /var/lib/mongodb/mongod.lock")
            call("mongod --repair")
            call("sudo service mongodb start")
        except Exception, e:
            print("That's work!")
            print(e)

    def update_hardware_module(self):
        # WATER LEVEL
        print self.enable_water_level
        if self.enable_water_level:
            self.hardware_water_sensor_process()

    def pre_process(self):
        if self.database.get(RedisDatabase.ENABLE_WATER_SENSOR) is None:
            self.database.set(RedisDatabase.ENABLE_WATER_SENSOR, True)
            self.enable_water_level = True;
        else:
            self.enable_water_level = bool(self.database.get(RedisDatabase.ENABLE_WATER_SENSOR));

    def hardware_water_sensor_process(self):
        global water_ranges

        with stopit.ThreadingTimeout(2) as to_ctx_mgr:
            assert to_ctx_mgr.state == to_ctx_mgr.EXECUTING
            water_ranges = self.ultra_sensor.get_perfect_rang()
            self.database.set_water_level(water_ranges)
            if self.debug:
                print("Water ranges = " + str(water_ranges))
        if to_ctx_mgr.state == to_ctx_mgr.TIMED_OUT:
            self.water_level_error_count += 1
            if self.water_level_error_count >= 5:
                self.database.set(RedisDatabase.ENABLE_WATER_SENSOR, False)
                self.enable_water_level = False
                Log.new(Log.ERROR, "Stop water level sensor ")

    # ##############################
    # ##########  Display ##########
    # ##############################

    def initial_display(self):
        print("Initial display process")
        try:
            self.TFT = TFT24T(spidev.SpiDev(), GPIO, landscape=True)
            self.TFT.initLCD(self.config.getint("GPIO", "DC"), self.config.getint("GPIO", "RST"),
                             self.config.getint("GPIO", "LED"), ce=1)
            self.draw = self.TFT.draw()
            self.TFT.clear((255, 255, 255))
            self.font = ImageFont.truetype('THSarabunNew.ttf', 24)
            self.display = DisplayScreen()
        except Exception, e:
            Log.new(Log.ERROR, "Initial display process error : " + str(e))

    # @fn_timer
    def display_main(self):
        self.TFT.load_wallpaper("bg.jpg")
        text = u'ระดับน้ำ :  {:10.4f} cm'
        text1 = u'อุณหภูมิ :'
        self.draw.text((10, 80), text1, fill=(32, 32, 32), font=self.font)
        self.draw_time()
        self.draw_ip()
        self.draw.text((10, 100), text.format(self.database.get_water_level()), fill=(32, 32, 32), font=self.font)
        self.draw.text((10, 120), str(self.database.get_screen_mode()), fill=(32, 32, 32), font=self.font)
        self.TFT.display()

    def _display_clear(self):
        self.TFT.clear()

    def draw_time(self):
        self.draw.text((170, 215), datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), fill=(32, 32, 32),
                       font=self.font)

    def draw_ip(self):
        self.draw.text((10, 215), self.ip, fill=(32, 32, 32), font=self.font)
