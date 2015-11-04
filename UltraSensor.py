import RPi.GPIO as GPIO
import time


class Ultra_sensor:
    GPIO_TRIGGER = None
    GPIO_ECHO = None
    OUT_OF_RANG = 100  # Rang for Error

    def __init__(self, trigger, echo):
        self.GPIO_ECHO = echo
        self.GPIO_TRIGGER = trigger
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)  # Trigger
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)  # Echo
        GPIO.output(self.GPIO_TRIGGER, False)
        # Allow module to settle
        time.sleep(0.5)

    def get_ultra_sensor_rang(self):
        total_distances = 0
        global x
        for x in range(0, 10):
            distance = self.get_pure_rang()
            if distance >= self.OUT_OF_RANG:
                continue
            if x > 0 and distance > 0:
                total_distances += distance
        return total_distances / x

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
