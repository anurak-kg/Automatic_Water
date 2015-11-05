from time import sleep

import System
import UltraSensor as UltraSensor

ultra = UltraSensor.Ultra_sensor(trigger=23, echo=24)
for i in range(1, 100):
    print ultra.get_ultra_sensor_rang()
    sleep(0.8)
System.GPIO.cleanup();
