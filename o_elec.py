import RPi.GPIO as GPIO
import pigpio
import sys

pi = pigpio.pi()


"""_____Global Variables_____"""
pi = pigpio.pi()
GPIO.setmode(GPIO.BCM)

"""_____Exception Class_____"""
class Unequal_PinState_Args(Exception):
    """ Raised when there are too many Pins or too many States to match the amount of another Argument
    """
    pass


"""_____Functions_____"""
"""Setup Pin(s)"""
def SetupOutput(*args):
    """
    Setup Pin(s) as OUTPUTs
    Pins will output as LOW
    """
    for pin in args:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
def SetupInput(*args):
    """
    Setup Pin(s) as INPUTs
    """
    for pin in args:
        GPIO.setup(pin, GPIO.IN)
def SetupHW_PWM(*args):
    # Setup Pins for HardWare PWM
    # PWM Configuration set for 0Hz and 0% Duty ; OFF Configuration
    for pin in args:
        pi.hardware_PWM(pin, 0, 0)

"""HardWare PWM"""
def ChangeHW_PWM(freq, duty, *args):
    # Configures all Pin arguments to a single PWM freq&duty value
    # CAN be used in place of SetupHW_PWM() function
    for pin in args:
        pi.hardware_PWM(pin, freq, duty)

"""GPIO Functions"""
def ReadInput(pin):
    # Read Pin State
    return GPIO.input(pin)
def ReadInputAll(*args):
    """
    Read Pin State of ALL pin parameters given
    Returns True if a SINGLE pin is HIGH
    Returns False if NO pin is HIGH
    CAN be used in place of ReadInput() function
    """
    for pin in args:
        if ReadInput(pin):
            return True
    return False
def ChangeOutput(pin, state):
    """
    Configures OUTPUT pin as HIGH or LOW.
    0=LOW ; 1=HIGH
    """
    if state == 1:
        GPIO.output(pin, GPIO.HIGH)
    elif state == 0:
        GPIO.output(pin, GPIO.LOW)
def ChangeOutputAll(lst_pin, lst_state):
    """
    Configures Pins in List to their respective States in List
    Raises Exception if amount of pins and state are not the same, then terminates program
    """
    try:
        if len(lst_pin) != len(lst_state):
            raise Unequal_PinState_Args
        else:
            for pin,state in zip(lst_pin, lst_state):
                ChangeOutput(pin, state)
    except Unequal_PinState_Args:
        print("Unequal amount of Pins and States")
        sys.exit()

"""Reset GPIO Pins"""
def ResetGPIO():
    """
    Resets ALL GPIO pins to their Original State
    """
    GPIO.cleanup()

"""_____Useful Functions_____"""
def Map(num, in_min, in_max, out_min, out_max):
    return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
