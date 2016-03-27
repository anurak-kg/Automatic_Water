import time

import RPi.GPIO as GPIO
import configparser
from Class.RedisDatabase import RedisDatabase
from Class.Timeout import TimeoutError


class UltraSensor:
    GPIO_TRIGGER = None
    GPIO_ECHO = None
    OUT_OF_RANG = 80  # Rang for Error
    TIME_OUT = 3  # Second time out

    def __init__(self, trigger, echo, number_of_sample=100):

        self.database = RedisDatabase()
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

        self.number_of_sample = number_of_sample
        self.GPIO_ECHO = echo
        self.GPIO_TRIGGER = trigger
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)  # Trigger
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)  # Echo
        GPIO.output(self.GPIO_TRIGGER, False)

    def get_ultra_sensor_rang(self):
        total_distances = 0
        i = int(1)
        list_distance = []
        error_count = 0
        while i < self.number_of_sample:
            try:
                if error_count >= 5:
                    print("Ultra sensor Time Out!")
                    return None
                distance = self.get_pure_rang()
                if distance >= self.OUT_OF_RANG:
                    continue
                if i >= 0 and 0 < distance < self.OUT_OF_RANG:
                    total_distances += distance
                i += 1
                list_distance.append(distance)
            except TimeoutError:
                error_count += 1
                print("Ultra sensor Time Out! +++++++++")

                return None

        # print min(list_distance)
        # print max(list_distance)

        return total_distances / i

    def get_perfect_rang(self, number_of_perfect=10):
        total_distances = 0
        i = int(0)
        list_distance = []
        while i <= number_of_perfect:
            try:
                distance = self.get_ultra_sensor_rang()
                if distance is None:
                    continue

                if distance >= self.OUT_OF_RANG:
                    continue

                if i >= 0 and 0 < distance < self.OUT_OF_RANG:
                    total_distances += distance

                i += 1
                list_distance.append(distance)
                time.sleep(0.01)

            except TimeoutError:
                print("Ultra sensor perfect time out!")
                return None

        # print min(list_distance)
        # print max(list_distance)

        return total_distances / i

    def get_pure_rang(self):
        global stop
        try:
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
        except UnboundLocalError:
            return None
