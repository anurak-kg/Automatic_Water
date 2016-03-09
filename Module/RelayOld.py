import RPi.GPIO as GPIO


class RelayOld:
    GPIO_WATER_IN = None
    GPIO_WATER_OUT = None
    GPIO_OTHER_1 = None
    GPIO_OTHER_2 = None

    def __init__(self, gpio_water_in=None, gpio_water_out=None, gpio_relay_1=None, gpio_relay_2=None):

        self.LIST_GPIO = None
        GPIO.setmode(GPIO.BCM)

        self.GPIO_WATER_IN = gpio_water_in
        self.GPIO_WATER_OUT = gpio_water_out
        self.GPIO_OTHER_1 = gpio_relay_1
        self.GPIO_OTHER_2 = gpio_relay_2

        if gpio_water_in is not None:
            GPIO.setup(gpio_water_in, GPIO.OUT)
            self.LIST_GPIO.append(gpio_water_in)

        if gpio_water_out is not None:
            GPIO.setup(gpio_water_out, GPIO.OUT)
            self.LIST_GPIO.append(gpio_water_in)

        if gpio_relay_1 is not None:
            GPIO.setup(gpio_relay_1, GPIO.OUT)
            self.LIST_GPIO.append(gpio_relay_1)

        if gpio_relay_2 is not None:
            GPIO.setup(gpio_relay_2, GPIO.OUT)
            self.LIST_GPIO.append(gpio_relay_2)

    def turn_on(self, gpio):
        if gpio is None:
            print "Error can't not found GPIO"
        else:
            GPIO.output(gpio, GPIO.HIGH)

    def turn_off(self, gpio):
        if gpio is None:
            print "Error can't not found GPIO"
        else:
            GPIO.output(gpio, GPIO.LOW)

    def clear_relay(self):
        for gpio in self.LIST_GPIO:
            self.turn_off(gpio)
        GPIO.cleanup()
