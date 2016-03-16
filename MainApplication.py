# coding=utf-8
import datetime
import os
import socket
import spidev
from time import sleep
import stopit

import RPi.GPIO as GPIO
import configparser
import traceback
from PIL import ImageFont
from subprocess import call

from Class import helper
from Class.Log import Log
from Class.RedisDatabase import RedisDatabase
from Class.Statistic import Statistic
from DisplayScreen import DisplayScreen
from Module.DHT11 import DHT11
from Module.UltraSensor import UltraSensor
from lib_tft24T import TFT24T

APP_VERSION = "0.0.1 Development  "


class MainApplication(object):
    def __init__(self):
        self.enable_dht11_sensor = True
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
        helper.initial_mongodb()
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
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("gmail.com", 80))
            self.ip = s.getsockname()[0]
            s.close()
        except Exception, e:
            self.ip = "No Internet connection"
            Log.new(Log.ERROR, "failed to find ip address")

    def initial_hardware_module(self):
        self.ultra_sensor = UltraSensor(echo=12, trigger=6, number_of_sample=10)

        self.dht11_error_count = 0
        self.dht11 = DHT11(gpio_dht=self.config.get("GPIO", "dht11"))

    def update_hardware_module(self):
        # WATER LEVEL Process
        print self.enable_water_level
        if self.enable_water_level:
            self.hardware_water_sensor_process()

        # DHT11 Sensor Process
        if self.enable_dht11_sensor:
            self.hardware_dht11_process()

    def pre_process(self):
        if self.database.get(RedisDatabase.ENABLE_WATER_SENSOR) is None:
            self.database.set(RedisDatabase.ENABLE_WATER_SENSOR, True)
            self.enable_water_level = True
        else:
            self.enable_water_level = bool(self.database.get(RedisDatabase.ENABLE_WATER_SENSOR))

    def hardware_water_sensor_process(self):
        global water_ranges

        with stopit.ThreadingTimeout(5) as to_ctx_mgr:
            assert to_ctx_mgr.state == to_ctx_mgr.EXECUTING

            water_ranges = self.ultra_sensor.get_perfect_rang()
            self.database.set_water_level(water_ranges)

            # clear error if working
            if self.water_level_error_count > 0:
                self.water_level_error_count -= 1

            if self.debug:
                print("  -Water ranges = " + str(water_ranges))

        if to_ctx_mgr.state == to_ctx_mgr.TIMED_OUT:
            self.water_level_error_count += 1
            self.database.set_water_level(-0)
            if self.water_level_error_count >= 5:
                self.database.set(RedisDatabase.ENABLE_WATER_SENSOR, False)
                self.enable_water_level = False
                Log.new(Log.ERROR, "Stop water level sensor ")

            # Debug water sensor
            if self.debug:
                print("water sensor time out")

    # DHT11 Process
    def hardware_dht11_process(self):
        with stopit.ThreadingTimeout(5) as to_ctx_mgr:
            assert to_ctx_mgr.state == to_ctx_mgr.EXECUTING
            (humidity, temperature) = self.dht11.get_temp_and_human()
            self.database.set(RedisDatabase.HUMIDITY, humidity)
            self.database.set(RedisDatabase.TEMPERATURE, temperature)
            # clear error if working
            if self.dht11_error_count > 0:
                self.dht11_error_count -= 1
            if self.debug:
                print("  -Humidity  = " + str(humidity))
                print("  -Temperature  = " + str(temperature))

        if to_ctx_mgr.state == to_ctx_mgr.TIMED_OUT:
            self.dht11_error_count += 1
            self.database.set(RedisDatabase.HUMIDITY, -0)
            self.database.set(RedisDatabase.TEMPERATURE, -0)

            if self.dht11_error_count >= 5:
                self.database.set(RedisDatabase.ENABLE_DHT_SENSOR, False)
                self.enable_dht11_sensor = False
                print("Dht11 error count = " + str(self.dht11_error_count))
                Log.new(Log.ERROR, "Stop dht11 sensor ")

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
        self.draw_time()
        self.draw_ip()
        title_font_color = (32, 32, 32)
        self.draw.text((10, 75), u'ระดับน้ำ :  {:6.2f} cm'.format(self.database.get_water_level()), title_font_color,
                       font=self.font)
        self.draw.text((10, 100), u'อุณหภูมิ : {:6.1f} °C'.format(float(self.database.get(RedisDatabase.TEMPERATURE))),
                       title_font_color, font=self.font)

        self.draw.text((10, 125), u'ความชื่น : {:6.1f} rH'.format(float(self.database.get(RedisDatabase.HUMIDITY))),
                       title_font_color, font=self.font)

        self.relay_section_draw()
        self.TFT.display()

    def _display_clear(self):
        self.TFT.clear()

    def draw_time(self):
        self.draw.text((170, 215), datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), fill=(32, 32, 32),
                       font=self.font)

    def draw_ip(self):
        self.draw.text((10, 215), self.ip, fill=(32, 32, 32), font=self.font)

    def relay_section_draw(self):
        x = 300
        y = 90
        r = 9
        text_x = 75
        for i in range(1, 5):
            self.draw.text((210, text_x), u"สวิทช์ " + str(i), fill=(32, 32, 32), font=self.font)
            self.draw.ellipse((x - r, y - r, x + r, y + r), fill="red")
            y += 25
            text_x += 25
