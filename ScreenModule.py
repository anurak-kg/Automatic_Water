# coding=utf-8
import threading
from time import sleep

import datetime

import socket
from PIL import ImageFont

from DisplayScreen import DisplayScreen
from lib_tft24T import TFT24T
from Database import Database
import RPi.GPIO as GPIO
import spidev


class ScreenModule(threading.Thread):
    def __init__(self, thread_id=None):
        super(ScreenModule, self).__init__()
        print("Screen Module Create")
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
        self.database = Database()
        self.database.set_screen_mode(DisplayScreen.MAIN)
        self._stop = threading.Event()

    def run(self):
        print("Start Thread!")
        self.database.set_screen_running(True)
        while self.database.get_screen_running():

            mode = self.database.get_screen_mode()
            if mode == DisplayScreen.MAIN:
                self.display_main()
            elif mode == DisplayScreen.CLEAR:
                self._display_clear()
        print("Stopped!")

    def display_main(self):
        self.TFT.load_wallpaper("bg.jpg")
        text = u'ระดับน้ำ : 2 '
        text1 = u'อุณหภูมิ :'
        self.draw.text((10, 80), text1, fill=(32, 32, 32), font=self.font)
        self.draw_time()
        self.draw_ip()
        self.draw.text((10, 100), text, fill=(32, 32, 32), font=self.font)
        self.draw.text((10, 120), str(self.database.get_screen_mode()), fill=(32, 32, 32), font=self.font)
        self.draw.textwrapped((10, 180), str(self.database.get_water_level()), 38, 10, self.font, fill=(32, 32, 32))
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
