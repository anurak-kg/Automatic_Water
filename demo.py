from time import sleep

from RPi import GPIO

from Module import UltraSensor

GPIO.cleanup()

# relay = Relay(gpio_relay_1=26)
#
# relay.turn_on(relay.GPIO_OTHER_1)
# sleep(1)
# relay.turn_off(relay.GPIO_OTHER_1)
rangSensor = UltraSensor.UltraSensor(echo=12, trigger=6)
while True:
    print "Rang = "
    print rangSensor.get_ultra_sensor_rang()
    sleep(1)
GPIO.cleanup()
