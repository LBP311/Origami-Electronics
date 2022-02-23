import touch_sensor
import RPi.GPIO as GPIO
import time
import sys

"""
Calls all functions within Touch Sensor Library.
"""

touch_sensor.setup()


try:
	while True:
		touch_sensor.Read_Pad0()
		time.sleep(1)

		touch_sensor.Read_Pad1()
		time.sleep(1)

		touch_sensor.Read_Pad2()
		time.sleep(1)

		touch_sensor.Read_Pad3()
		time.sleep(1)

		touch_sensor.Read_Pad4()
		time.sleep(1)

		touch_sensor.Read_All()
		time.sleep(1)

except KeyboardInterrupt:
	GPIO.cleanup()
	sys.exit()
