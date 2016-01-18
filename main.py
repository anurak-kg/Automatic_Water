from time import sleep

from Database import Database
from ScreenModule import ScreenModule

print("Start Process")

screen = ScreenModule()
try:
    screen.start()
except KeyboardInterrupt:
    screen._stop()

print("Start Main Thread")
database = Database()
database.set_water_level(20)
try:
    while True:
        sleep(3)
except KeyboardInterrupt:
    database.set_screen_running(False)
    print("Exit")
