from math import floor, ceil

import RPi.GPIO as GPIO
import time

import helper
from collections import Counter


class UltraSensor:
    GPIO_TRIGGER = None
    GPIO_ECHO = None
    OUT_OF_RANG = 80  # Rang for Error
    TIME_OUT = 3  # Second time out

    def __init__(self, trigger, echo, number_of_sample=100):
        self.number_of_sample = number_of_sample
        self.GPIO_ECHO = echo
        self.GPIO_TRIGGER = trigger
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)  # Trigger
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)  # Echo
        GPIO.output(self.GPIO_TRIGGER, False)
        # Allow module to settle
        time.sleep(0.5)

    def get_ultra_sensor_rang(self):
        time_out = time.time() + self.TIME_OUT
        total_distances = 0
        i = int(0)
        list_distance = []
        while i < self.number_of_sample:
            distance = self.get_pure_rang()
            if time.time() > time_out:
                print("Ultra sensor Time Out!")
                return 0

            if distance >= self.OUT_OF_RANG:
                continue
            if i >= 0 and 0 < distance < self.OUT_OF_RANG:
                total_distances += distance
                i += 1
                list_distance.append(distance)

        # print min(list_distance)
        # print max(list_distance)

        return total_distances / i

    def get_pure_rang(self):
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
