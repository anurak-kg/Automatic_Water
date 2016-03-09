# coding=utf-8
import datetime
import socket
import spidev
import threading
from time import sleep

import RPi.GPIO as GPIO
from PIL import ImageFont

from Class.RedisDatabase import RedisDatabase
from Class.Timeout import TimeoutError
from DisplayScreen import DisplayScreen
from Module.UltraSensor import UltraSensor
from helper import fn_timer
from lib_tft24T import TFT24T


class ScreenModule(threading.Thread):
    def __init__(self, thread_id=None):
        super(ScreenModule, self).__init__()

        self.enable_water_level = True

        self.thread_id = thread_id

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        dc = 22
        rst = 18
        led = 23

        self.TFT = TFT24T(spidev.SpiDev(), GPIO, landscape=True)

        self.TFT.initLCD(dc, rst, led, ce=1)
        self.init_ip()

        self.draw = self.TFT.draw()
        self.TFT.clear((255, 255, 255))
        self.font = ImageFont.truetype('THSarabunNew.ttf', 24)

        self.display = DisplayScreen()
        self.database = RedisDatabase()
        self.database.set_screen_mode(DisplayScreen.MAIN)
        self._stop = threading.Event()

        self.initial_hardware_module()

    def run(self):
        print("Start Main Thread!")
        self.database.set_app_running(True)
        while self.database.get_app_running():

            mode = self.database.get_screen_mode()
            if mode == DisplayScreen.MAIN:
                self.display_main()
            elif mode == DisplayScreen.CLEAR:
                self._display_clear()
            sleep(1)
        print("Stopped!")

    @fn_timer
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

    def init_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com", 80))
        self.ip = s.getsockname()[0]
        s.close()

    def initial_hardware_module(self):
        self.ultra_sensor = UltraSensor(echo=12, trigger=6, number_of_sample=10)

    def update_hardware_module(self):
        global water_ranges
        if self.enable_water_level:
            try:
                water_ranges = self.ultra_sensor.get_perfect_rang()
            except TimeoutError:
                water_ranges = None
                print "Update hardware timeout!!"
                sleep(5)
        self.database.set_water_level(water_ranges)
        print("Water ranges = " + str(water_ranges))
