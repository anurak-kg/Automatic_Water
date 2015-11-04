import time
import RPi.GPIO as GPIO
import Adafruit_DHT
from datetime import datetime
from w1thermsensor import W1ThermSensor
import helper

__author__ = 'Anurak'


class SystemProject(object):
    def __init__(self):
        pass

    relay_list = []
    sensor_water = None
    GPIO_TRIGGER = None
    GPIO_ECHO = None
    DHT = Adafruit_DHT.DHT11
    GPIO_TEMP = None
    ENABLE_WATER_TEMP = False
    ENABLE_ULTRA_SENSOR = False
    ENABLE_TEMP = False
    ENABLE_RELAY = False
    RELAY = []
    IN_GPIO = [None, None, None, None]
    relay_dict = None

    def setup(self):
        if self.GPIO_TRIGGER is not None:
            self.setup_ultra_sensor()
        if self.ENABLE_WATER_TEMP:
            self.setup_water_temp()
        if self.ENABLE_RELAY:
            self.setup_relay()

    def set_ultra_sensor(self, dht_version, trigger, echo):
        self.GPIO_ECHO = echo
        self.DHT = dht_version
        self.GPIO_TRIGGER = trigger
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)  # Trigger
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)  # Echo

    def setup_ultra_sensor(self):
        GPIO.setmode(GPIO.BCM)
        # Set trigger to False (Low)
        GPIO.output(self.GPIO_TRIGGER, False)

    def setup_water_temp(self):
        self.sensor_water = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20)

    def get_ultra_sensor(self):
        distance = -0
        if self.ENABLE_ULTRA_SENSOR:
            GPIO.output(self.GPIO_TRIGGER, True)
            time.sleep(0.00001)
            GPIO.output(self.GPIO_TRIGGER, False)
            start = time.time()
            while GPIO.input(self.GPIO_ECHO) == 0:
                start = time.time()

            while GPIO.input(self.GPIO_ECHO) == 1:
                stop = time.time()

            # Calculate pulse length
            elapsed = stop - start

            # Distance pulse travelled in that time is time
            # multiplied by the speed of sound (cm/s)
            distance = elapsed * 34000

            # That was the distance there and back so halve the value
            distance /= 2
        return distance

    @staticmethod
    def cleanup():
        GPIO.cleanup()

    def get_temp_and_human(self):
        if self.ENABLE_TEMP:
            return Adafruit_DHT.read_retry(self.DHT, self.GPIO_TEMP)
        else:
            return -0, -0

    def get_water_temp(self):
        return self.sensor_water.get_temperature()

    def set_enable_water_temp(self, status):
        self.ENABLE_WATER_TEMP = status

    def set_enable_ultra_sensor(self, status):
        self.ENABLE_ULTRA_SENSOR = status

    def set_enable_temp(self, status):
        self.ENABLE_TEMP = status

    def set_enable_relay(self, status):
        self.ENABLE_RELAY = status

    def set_relay_enable(self, status):
        self.IN_GPIO = 0

    def add_relay(self, gpio):
        self.relay_list.append({'gpio': gpio, 'current_status': False})
        GPIO.setup(gpio, GPIO.OUT)
        GPIO.output(gpio, GPIO.LOW)
        self.relay_dict = helper.build_dict(self.relay_list, 'gpio')

    def relay_set_status(self, gpio, status):
        self.relay_list[self.relay_get_index(gpio)]['current_status'] = status

    def get_relay_status(self, gpio):
        return self.relay_list[self.relay_get_index(gpio)]['current_status'];

    def relay_get_index(self, gpio):
        return self.relay_dict[gpio]['index']

    def turn_on_relay(self, gpio):
        GPIO.output(gpio, GPIO.HIGH)
        self.relay_set_status(gpio, True)

    def turn_off_relay(self, gpio):
        GPIO.output(gpio, GPIO.LOW)
        self.relay_set_status(gpio, False)

    @staticmethod
    def relay_get_state(gpio):
        return GPIO.input(gpio)

    def setup_relay(self, gpios):
        GPIO.setmode(GPIO.BCM)
        if gpios is not None:
            for gpio in gpios:
                self.add_relay(gpio)

    @staticmethod
    def timer_check(start, end):
        if helper.time_in_range(start, end):
            return True
        else:
            return False
