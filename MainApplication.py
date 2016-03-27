# coding=utf-8
import stopit
import RPi.GPIO as GPIO
import configparser
import traceback
from time import sleep, time
from PIL import ImageFont
from Class import helper
from Class.Log import Log
from Class.RedisDatabase import RedisDatabase
from Class.Statistic import Statistic
from Class.Timer import Timer
from DisplayScreen import DisplayScreen
from Module.DHT11 import DHT11
from Module.Display import Display
from Module.UltraSensor import UltraSensor


APP_VERSION = "0.0.1 Development  "


class MainApplication(object):
    def __init__(self):
        self.enable_dht11_sensor = True
        self.water_level_error_count = 0
        self.debug = False

        print("###################################")
        print("#######       Welcome       #######")
        print("####### " + APP_VERSION + " #######")
        print("###################################")

        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.database = RedisDatabase()

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.pre_process()
        self.database.set_screen_mode(DisplayScreen.MAIN)

        self.initial_hardware_module()
        helper.initial_mongodb()
        self.statistic = Statistic()
        self.display = Display(self.database, self.config)
        self.start_timer_thread()
        # self.webserver = Test()
        # self.webserver.start()
        self.start()

    def start(self):
        print("### Start Main Thread!")
        self.database.set_app_running(True)

        while self.database.get_app_running():
            start_time = time()

            self.display.display_main()

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
            elapsed_time = time() - start_time

            if self.debug:
                print("time process in " + str(elapsed_time) + " sec")
                # sleep(1)
        print("Stopped!")

    def initial_hardware_module(self):
        self.ultra_sensor = UltraSensor(echo=12, trigger=6, number_of_sample=10)

        self.dht11_error_count = 0
        self.dht11 = DHT11(gpio_dht=self.config.get("GPIO", "dht11"))

    def update_hardware_module(self):
        # WATER LEVEL Process
        if self.debug:
            print("water level enable us " + str(self.enable_water_level))

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

    def start_timer_thread(self):
        try:
            timer = Timer(config=self.config, redis_database=self.database)
            timer.start()
        except Exception, e:
            print("ERROR start_timer_thread() 0x00003")
            Log.new(Log.ERROR, "ERROR start_timer_thread 0x00003")
            Log.new(Log.ERROR, "" + str(e))

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
