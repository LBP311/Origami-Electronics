import RPi.GPIO as GPIO

def setup():
	print("All peripherals and sensors have been set up successfully!")
	return True


"""
Note:
Only 1 Touch Pad can be used at a time.
Wrote read_all() to check which pad is activated when called.
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
