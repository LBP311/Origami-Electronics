import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#Pins= [Pad0, Pad1, Pad2, Pad3, Pad4]
PADS = [24, 23, 18, 15, 14]	# Touch Pad BCM Pins ; Use NoneType if Pad is not in use

def setup():
	global PADS

	for pin in PADS:
		if (pin is not None):
			GPIO.setup(pin, GPIO.IN)

	print("All pins have been set up successfully!")
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


Read_Pad(input) function is used to know if Pad# is ON/OFF for use in greater applications.

Read_All() function would check for which Pad# is activated when called.

Wait_All() function is used to implement interrupts for all the Touch Pads.

Wait_Pad(input) functin is used to implement an interrupt for the specified Touch Pad.
"""


# Read State of Pad#
def Read_Pad(input):
	"""
	Accepts pad # to read state.
	Returns Pad state
	State: 1 = Not Active
	       0 = Active
	       None = Incorrect Pad # / Pad not setup
	"""
	global PADS

	if (PADS[input] is not None):
		return GPIO.input(PADS[input])
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

# Create Interrupt for Pad#
def Wait_Pad(input):
	global PADS

	if (PADS[input] is not None):
		GPIO.add_event_detect(PADS[input], GPIO.FALLING)
		print("Pad Interrupt " + str(input) + " setup correctly!")
		return True
	print("Touch Pad " + str(input) + " is not setup...")
	return False


# Create Interrupts for all Pads
def Wait_All():
	for pad in range(5):
		Wait_Pad(pad)
	return True

