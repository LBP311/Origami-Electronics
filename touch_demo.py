from touch_sensor import *
import RPi.GPIO as GPIO
import time
import sys

"""
Calls all functions within Touch Sensor Library.
touch_sensor.py
"""

"""
try:

	print("Setup")
	setup()

	print("\nRead_Pad")
	# 10 Tests: 5 Pad Touches and 5 Pad with No Touch
	for i in range(10):
		pad = int(input("Enter Pad /#:"))

		if (Read_Pad(pad)):
			print("Not Active")
		else:
			print("Active")
		time.sleep(1)

	print("\nRead_All")
	# 6 Tests: 5 Pad Touches and No Touch
	for i in range(6):
		active = Read_All()
		if (active is not None):
			print("Active Pad: " + str(active))
		else:
			print("None Active")
		time.sleep(5)


	print("\nWait_Pad")
	for pad in range (5):
		Wait_Pad(pad)

	while True:
		if GPIO.event_detected(PADS[0]):
			print("Detected 0")
		if GPIO.event_detected(PADS[1]):
			print("Detected 1")
		if GPIO.event_detected(PADS[2]):
			print("Detected 2")
		if GPIO.event_detected(PADS[3]):
			print("Detected 3")
		if GPIO.event_detected(PADS[4]):
			print("Detected 4")

except KeyboardInterrupt:
	GPIO.cleanup()
	sys.exit()
"""


try:
	print("Setup")
	setup()

	print("\nWait_All")
	Wait_All()

	while True:
		if GPIO.event_detected(PADS[0]):
			print("Detected 0")
		if GPIO.event_detected(PADS[1]):
			print("Detected 1")
		if GPIO.event_detected(PADS[2]):
			print("Detected 2")
		if GPIO.event_detected(PADS[3]):
			print("Detected 3")
		if GPIO.event_detected(PADS[4]):
			print("Detected 4")

except KeyboardInterrupt:
	GPIO.cleanup()
	sys.exit()


	
