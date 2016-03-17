# coding=utf-8
import socket
import threading

import spidev

import datetime
from PIL import ImageFont
from RPi import GPIO

from Class.Log import Log
from Class.RedisDatabase import RedisDatabase
from lib_tft24T import TFT24T


class Display:
    def __init__(self, database, config):
        self.font = ImageFont.truetype('THSarabunNew.ttf', 24)
        self.TFT = TFT24T(spidev.SpiDev(), GPIO, landscape=True)


        self.config = config
        self.initial_display()
        self.draw = self.TFT.draw()
        self.database = database
        self.init_ip()
        self.ip = None

    def init_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("gmail.com", 80))
            self.ip = s.getsockname()[0]
            s.close()
        except Exception, e:
            self.ip = "No Internet connection"
            Log.new(Log.ERROR, "failed to find ip address")
            print(e)

    def initial_display(self):
        print("Initial display process")
        try:
            self.TFT.initLCD(self.config.getint("GPIO", "DC"), self.config.getint("GPIO", "RST"),
                             self.config.getint("GPIO", "LED"), ce=1)
            self.TFT.clear((255, 255, 255))
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
        pass
        # self.draw.text((10, 215), self.ip, fill=(32, 32, 32), font=self.font)

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