from w1thermsensor import W1ThermSensor


class WaterTemperature:
    def __init__(self):
        self.sensor_water = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20)

    def get_temperature(self):
        return self.sensor_water.get_temperature()
