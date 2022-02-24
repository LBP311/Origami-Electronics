import RPi.GPIO as GPIO
import pigpio
import sys

pi = pigpio.pi()
GPIO.setmode(GPIO.BCM)

B_Pin = 13	# BCM 13 ; PWM 0

pi.hardware_PWM(B_Pin, 5000, 500000)


try:
	while True:
		continue
except KeyboardInterrupt:
	pi.hardware_PWM(B_Pin, 0, 0)
	sys.exit()
