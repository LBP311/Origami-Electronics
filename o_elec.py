import RPi.GPIO as GPIO
import pigpio
import time
import sys

from Notes import *
from Songs import *

pi = pigpio.pi()
GPIO.setmode(GPIO.BCM)



"""===========___Global Variables___==========="""

"""___Touch Sensor___"""
#TouchPad# = [T0, T1, T2, T3, T4]
TOUCH_PINS = [None, None, None, None, None]	# Touch PAd BCM Pins ; Use NoneType if Pad is not in use

"""___Buzzer___"""
BUZZ_PIN = 13		# Buzzer BCM Pin
BUZZ_DUTY = 500000	# 50% PWM Duty Cycle (KEEP CONSTANT!!!!!)
TEMPO = 144		# Dictates Speed of Song Playing (Higher = Faster) (Lower = Slower)
WHOLENOTE = (60 * 4) / TEMPO	# Length of Time that a Whole Note is played

"""___LED Globals___"""
LED_PIN = None

"""___Motor Globals___"""
MOTOR_PIN = None
M_PWM = 0		# From 0Hz to 5kHz ; (Based on Personal Comfortability. Feel free to increase the MAX Freq.)
M_DUTY = 500000		# Will keep at 50% Duty to regulate Vibration ; (Based on Personal Comfortability. Feel free to adjust according to your needs.)
M_LEVEL = 0



"""===========___Functions___==========="""
def setup():
	global TOUCH_PINS
	global BUZZ_PIN
	global BUZZ_DUTY
	global LED_PIN
	global MOTOR_PIN
	global M_DUTY
	"""
	# Setup Touch Sensor
	for pin in TOUCH_PINS:
		if (pin is not None):
			GPIO.setup(pin, GPIO.IN)

	# Setup LED Connections
	GPIO.setup(LED_PIN, GPIO.OUT)
	GPIO.output(LED_PIN, GPIO.LOW)

	# Setup Motor
	pi.hardware_PWM(MOTOR_PIN, REST, M_DUTY)	# REST = 0Hz (Motor OFF)
	# Setup Buzzer
	pi.hardware_PWM(BUZZ_PIN, REST, BUZZ_DUTY)	# REST = 0Hz (Buzzer OFF)
	"""
	print("All pins have been set up successfully!")
	return True


"""___Touch Pad Functions___"""
# Read State of Pad#
def ReadPad(input):
	"""
	Accepts pad # to read state.
	Retrurns Pad State.
	States: None = Incorrect Pad # / Pad not setup
		1 = Not Active
		0 = Active
	"""
	global TOUCH_PINS
	"""
	if (TOUCH_PINS[input] is not None):
		return GPIO.input(TOUCH_PINS[input])
	return None
	"""
	print("ReadPad#")

# Search for Activated Pad
def ReadAll():
	"""
	Reads all pad states.
	Returns pad# of active pad.
	If none are active, return None.
	"""
	"""
	for pad in range(5):
		if (ReadPad(pad) == 0):
			return pad
	return None
	"""
	print("ReadAll")

# Wait Until Pad# is Activated
def WaitPad(input):
	global TOUCH_PINS
	"""
	if (TOUCH_PINS[input] is not None):
		GPIO.wait_for_edge(TOUCH_PINS[input], GPIO.FALLING)
	"""
	print("WaitPad")

# Wait until correct Pads are Activated in Sequence
def WaitPadSequence(seq_lst):
	"""
	for pad in seq_lst:
		WaitPad(pad)
	"""
	print("WaitPadSequence")


"""___Buzzer Functions___"""
def PlaySong(song):
	global WHOLENOTE
	global BUZZ_PIN
	global BUZZ_DUTY
	"""
	if (song == "TETRIS"):
		song = TETRIS
	elif (song == "BIRTHDAY"):
		song = BIRTHDAY
	else:
		song = P_PANTHER

	for i in range(0, int(len(song)), 2):
		divisor = song[i+1]
		if (divisor > 0):
			noteDuration = WHOLENOTE / divisor
		elif (divisor < 0):		# Dotted Notes have a Negative Divisor
			noteDuration = WHOLENOTE / (-divisor)
			noteDuration *= 1.5
		print(str(song[i]) + "\t" + str(noteDuration))
		pi.hardware_PWM(BUZZ_PIN, song[i], BUZZ_DUTY)
		time.sleep(noteDuration*0.9)
		pi.hardware_PWM(BUZZ_PIN, REST, BUZZ_DUTY)
		time.sleep(noteDuration*0.1)
	"""
	print("PlaySong")

# Play a Specific Note for given Seconds
def PlayNote(note, octave, duration):
	global BUZZ_PIN
	global BUZZ_DUTY
	"""
	pi.hardware_PWM(BUZZ_PIN, note, BUZZ_DUTY)
	time.sleep(duration)
	"""
	print("PlayNote")


"""___LED Functions___"""
def LED_ON():
	"""
	global LED_PIN
	pi.hardware_PWM(LED_PIN, 250000, 1000000)
	"""
	print("LED_ON")

def LED_OFF():
	"""
	global LED_PIN
	pi.hardware_PWM(LED_PIN, REST, REST)
	"""
	print("LED_OFF")


"""___Motor Functions___"""
def MotorVibLevel(level):
# Changes Vibration Level
# Saves Current Settings
	global MOTOR_PIN
	global M_PWM
	global M_DUTY
	"""
	M_PWM = (5000/5)*level
	pi.hardware_PWM(MOTOR_PIN, M_PWM, M_DUTY)
	"""
	M_PWM = (5000/5)*level
	print("Current PWM Freq = " + str((5000/5)*level) + "\tDuty = " + str(M_DUTY))

def MotorOFF():
	global MOTOR_PIN
	global M_DUTY
	"""
	pi.hardware_PWM(MOTOR_PIN, 0, M_DUTY)
	"""
	print("Motor OFF")

def MotorON():
# Will use the Settings previously configured
# Settings can be configured through MotorVibLevel
	global MOTOR_PIN
	global M_PWM
	global M_DUTY
	"""
	pi.hardware_PWM(MOTOR_PIN, M_PWM, M_DUTY)
	"""
	print("Current/Previous Settings: " + str(M_PWM) + "\tDuty = " + str(M_DUTY))
