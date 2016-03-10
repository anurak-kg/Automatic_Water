import Adafruit_DHT


class DHT:
    def __init__(self, sensor_version=Adafruit_DHT.DHT11, gpio_dht=0):
        self.gpio_dht = gpio_dht
        self.sensor_version = sensor_version

    def get_temp_and_human(self):
        if self.gpio_dht != 0:
            return Adafruit_DHT.read_retry(self.sensor_version, self.gpio_dht)
        else:
            return -0, -0
