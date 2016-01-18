# coding=utf-8
import WaterChanger
from PIL import Image
from PIL import ImageFont
from lib_tft24T import TFT24T
from Database import Database
import RPi.GPIO as GPIO
import spidev

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


DC = 22
RST = 18
LED = 23

TFT = TFT24T(spidev.SpiDev(), GPIO, landscape=True)

TFT.initLCD(DC, RST, LED, ce=1)
draw = TFT.draw()
TFT.clear((255, 255, 255))
database = Database()
database.test_connect()
#  # Image of calculator !!!
font = ImageFont.truetype('THSarabunNew.ttf', 22)
i = 1
while True:
    TFT.load_wallpaper("bg.jpg")
    text = u'ระดับน้ำ : 2 '

    text1 = u'อุณหภูมิ :'
    draw.text((10, 80), text1, fill=(32, 32, 32), font=font)
    draw.text((10, 100), text, fill=(32, 32, 32), font=font)
    draw.text((10, 120), str(i), fill=(32, 32, 32), font=font)
    draw.textwrapped((10, 140), str(i), 38, 10, font, fill=(32, 32, 32))
    TFT.display()
    i += 1
# water_changer = WaterChanger.WaterChanger(min_water_level=5, max_water_level=2)
# water_changer.start();
