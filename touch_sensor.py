import RPi.GPIO as GPIO

def setup():
	print("All peripherals and sensors have been set up successfully!")
	return True


"""
Note:
Since only 1 Touch Pad can be used at a time, I chose to create functions which respond to their individual Pads.
I also thought that we may not know which pad is being used or may just want to check all the pads so I created 
another function which would check for which pad was activated.

Read_Pad#() functions are to be used to know if Pad# is ON/OFF for use in greater applications.

Read_All() function would check for which Pad# is activated when called.
"""


# Only read Touch Pad 0
def Read_Pad0():
	print("Touch Pad 0")

# Only read Touch Pad 1
def Read_Pad1():
	print("Touch Pad 1")

# Only read Touch Pad 2
def Read_Pad2():
	print("Touch Pad 2")

# Only read Touch Pad 3
def Read_Pad3():
	print("Touch Pad 3")

# Only read Touch Pad 4
def Read_Pad4():
	print("Touch Pad 4")

# Search for which pad is activated
def Read_All():
	print("All Pads")
