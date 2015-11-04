import System
import UltraSensor as UltraSensor

ultra = UltraSensor.Ultra_sensor(trigger=23, echo=24)
print ultra.get_ultra_sensor_rang()
System.GPIO.cleanup();