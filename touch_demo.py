import touch_sensor
import RPi.GPIO as GPIO
import time
import sys

"""
Calls all functions within Touch Sensor Library.
touch_sensor.py
"""

touch_sensor.setup()


try:
	while True:
		for i in range(6):
			pad = int(input("Enter Pad \#:"))

			if (touch_sensor.Read_Pad(pad)):
				print("Not Active")
			else:
				print("Active")
			time.sleep(2)

			print("Read-All")
			active = touch_sensor.Read_All()
			if (active is not None):
				print("Active Pad: " + str(active))
			else:
				print("None Active")

except KeyboardInterrupt:
	GPIO.cleanup()
	sys.exit()
