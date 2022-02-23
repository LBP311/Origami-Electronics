import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

P0 = 1
P1 = 12
P2 = 16
P3 = 20
P4 = 21

def setup():
	print("All peripherals and sensors have been set up successfully!")

	GPIO.setup(P0, GPIO.IN)
	GPIO.setup(P1, GPIO.IN)
	GPIO.setup(P2, GPIO.IN)
	GPIO.setup(P3, GPIO.IN)
	GPIO.setup(P4, GPIO.IN)

	return True


"""
Note:
Since only 1 Touch Pad can be used at a time, I chose to create functions which respond to their individual Pads.
I also thought that we may not know which pad is being used or may just want to check all the pads so I created 
another function which would check for which pad was activated.

Filled in functions for testing purposes.
GPIO input of each pad is HIGH when untouched. LOW when touched.
Functions test for when the Pad is LOW.
Attempted to touch multiple pads and as expected, only 1 pad can be used at any given time.


Read_Pad#() functions are to be used to know if Pad# is ON/OFF for use in greater applications.

Read_All() function would check for which Pad# is activated when called.
"""


# Only read Touch Pad 0
def Read_Pad0():
	print("Touch Pad 0")

	if (GPIO.input(P0) == 0):
		print("HIT")
	else:
		print("MISS")

# Only read Touch Pad 1
def Read_Pad1():
	print("Touch Pad 1")

	if (GPIO.input(P1) == 0):
		print("HIT")
	else:
		print("MISS")

# Only read Touch Pad 2
def Read_Pad2():
	print("Touch Pad 2")

	if (GPIO.input(P2) == 0):
		print("HIT")
	else:
		print("MISS")

# Only read Touch Pad 3
def Read_Pad3():
	print("Touch Pad 3")

	if (GPIO.input(P3) == 0):
		print("HIT")
	else:
		print("MISS")

# Only read Touch Pad 4
def Read_Pad4():
	print("Touch Pad 4")

	if (GPIO.input(P4) == 0):
		print("HIT")
	else:
		print("MISS")

# Search for which pad is activated
def Read_All():
	print("All Pads")

	if (GPIO.input(P0) == 0):
		print("Pad 0")
	elif (GPIO.input(P1) == 0):
		print("Pad 1")
	elif (GPIO.input(P2) == 0):
		print("Pad 2")
	elif (GPIO.input(P3) == 0):
		print("Pad 3")
	elif (GPIO.input(P4) == 0):
		print("Pad 4")
	else:
		print("MISS")
