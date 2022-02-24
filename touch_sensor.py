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
Since only 1 Touch Pad can be used at a time, I chose to create a function which responds to the corresponding Pad.
I also thought that we may not know which pad is being used or may just want to check all the pads so I created
another function which would check for which pad was activated.

Filled in functions for testing purposes.
GPIO input of each pad is HIGH when untouched. LOW when touched.
Functions test for when the Pad is LOW.
Attempted to touch multiple pads and as expected, only 1 pad can be used at any given time.


Read_Pad() function is used to know if Pad# is ON/OFF for use in greater applications.

Read_All() function would check for which Pad# is activated when called.
"""


# Read Pad#
def Read_Pad(pad):
	"""
	Accepts pad # to read state.
	Returns Pad state
	State: 1 = Not Active
	       0 = Active
	       None = Incorrect Pad #
	"""

	if (pad == 0):
		return GPIO.input(P0)
	elif (pad == 1):
		return GPIO.input(P1)
	elif (pad == 2):
		return GPIO.input(P2)
	elif (pad == 3):
		return GPIO.input(P3)
	elif (pad == 4):
		return GPIO.input(P4)
	return None

# Search for which pad is activated
def Read_All():
	"""
	Reads all pad states.
	Returns pad# of active pad.
	If none are active, return None.
	"""

	for pad in range(5):
		if (Read_Pad(pad) == 0):
			return pad
	return None
