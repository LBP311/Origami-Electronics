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
	touch_sensor.Wait_Pad(0)
	touch_sensor.Wait_Pad(1)
	touch_sensor.Wait_Pad(2)
	touch_sensor.Wait_Pad(3)
	touch_sensor.Wait_Pad(4)

#	while True:
#		continue

	"""
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
	"""

except KeyboardInterrupt:
	GPIO.cleanup()
	sys.exit()
