import RPi.GPIO as GPIO
import pigpio
import time

from Notes import *     # Contains Note Frequencies used for each song
from threading import Event     # Used for Threading, if needed

pi = pigpio.pi()


""" Globals for Playing Songs """
TEMPO = 140     # Average Song Tempo ; Higher Value=Faster Song ; Lower Value=Slower Song
WHOLENOTE = (60 * 4) / TEMPO    # Determines Beat Lengths for Songs

# Songs are best played at 50% Duty Cycle
HW_PWM_DUTY = 500000    # !!! DO NOT RECOMMEND CHANGING!!!

# Used for Threading ; Initially Set if Threading is not used
# If Threading is not used ; Ignore it
ePLAYSONG = Event()
ePLAYSONG.set()


""" Current Songs """
# Includes Notes and Beat Lengths
# 1=Wholenote ; 2=Halfnote ; 4=Quarter Note; 8=Eighth Note
# Negative Beat Lengths are 1.5times longer
CANON = [FS4, 2, E4, 2, D4, 2, CS4, 2, B3, 2, A3, 2, B3, 2, CS4, 2,
		B3, 2, A3, 2, B3, 2, CS4, 2, D4, 2, CS4, 2, B3, 2, A3, 2,
		G3, 2, FS3, 2, G3, 2, A3, 2,
	D4, 4, FS4, 8, G4, 8, A4, 4, FS4, 8, G4, 8, A4, 4, B3, 8, CS4, 8, D4, 8, E4, 8, FS4, 8, G4, 8,
	FS4, 4, D4, 8, E4, 8, FS4, 4, FS3, 8, G3, 8, A3, 8, G3, 8, FS3, 8, G3, 8, A3, 2,
	G3, 4, B3, 8, A3, 8, G3, 4, FS3, 8, E3, 8, FS3, 4, D3, 8, E3, 8, FS3, 8, G3, 8, A3, 8, B3, 8,
	G3, 4, B3, 8, A3, 8, B3, 4, CS4, 8, D4, 8, A3, 8, B3, 8, CS4, 8, D4, 8, E4, 8, FS4, 8, G4, 8, A4, 2,
	A4, 4, FS4, 8, G4, 8, A4, 4, FS4, 8, G4, 8, A4, 8, A3, 8, B3, 8, CS4, 8,
	D4, 8, E4, 8, FS4, 8, G4, 8, FS4, 4, D4, 8, E4, 8, FS4, 8, CS4, 8, A3, 8, A3, 8,
	CS4, 4, B3, 4, D4, 8, CS4, 8, B3, 4, A3, 8, G3, 8, A3, 4, D3, 8, E3, 8, FS3, 8, G3, 8,
	A3, 8, B3, 4, G3, 4, B3, 8, A3, 8, B3, 4, CS4, 8, D4, 8, A3, 8, B3, 8, CS4, 8, D4, 8, E4, 8,
	FS4, 8, G4, 8, A4, 2]

TETRIS = [E5, 4, B4, 8, C5, 8, D5, 4, C5, 8, B4, 8,
		A4, 4, A4, 8, C5, 8, E5, 4, D5, 8, C5, 8,
		B4, -4, C5, 8, D5, 4, E5, 4,
		C5, 4, A4, 4, A4, 8, A4, 4, B4, 8, C5, 8,
	  D5, -4, F5, 8, A5, 4, G5, 8, F5, 8,
		E5, -4, C5, 8, E5, 4, D5, 8, C5, 8,
		B4, 4, B4, 8, C5, 8, D5, 4, E5, 4,
		C5, 4, A4, 4, A4, 4, REST, 4,
	  E5, 4, B4, 8, C5, 8, D5, 4, C5, 8, B4, 8,
		A4, 4, A4, 8, C5, 8, E5, 4, D5, 8, C5, 8,
		B4, -4, C5, 8, D5, 4, E5, 4,
		C5, 4, A4, 4, A4, 8, A4, 4, B4, 8, C5, 8,
	  D5, -4, F5, 8, A5, 4, G5, 8, F5, 8,
		E5, -4, C5, 8, E5, 4, D5, 8, C5, 8,
		B4, 4, B4, 8, C5, 8, D5, 4, E5, 4,
		C5, 4, A4, 4, A4, 4, REST, 4,
	  E5, 2, C5, 2, D5, 2, B4, 2, C5, 2, A4, 2,
		GS4, 2, B4, 4, REST, 8, E5, 2, C5, 2, D5, 2, B4, 2,
		C5, 4, E5, 4, A5, 2, GS5, 2]

BIRTHDAY = [C4, 4, C4, 8, D4, -4, C4, -4, F4, -4,
		E4, -2, C4, 4, C4, 8, D4, -4, C4, -4,
		G4, -4, F4, -2, C4, 4, C4, 8,
	    C5, -4, A4, -4, F4, -4, E4, -4, D4, -4,
		AS4, 4, AS4, 8, A4, -4, F4, -4, G4, -4,
		F4, -2]

P_PANTHER = [REST, 2, REST, 4, REST, 8, DS4, 8,
		E4, -4, REST, 8, FS4, 8, G4, -8, REST, 8, DS4, 8,
		E4, -8, FS4, 8, G4, -8, C5, 8, B4, -8, E4, 8, G4, -8, B4, 8,
		AS4, 2, A4, -16, G4, -16, E4, -16, D4, -16, E4, 2, REST, 4,
		REST, 8, DS4, 4,
	     E4, -4, REST, 8, FS4, 8, G4, -4, REST, 8, DS4, 8,
		E4, -8, FS4, 8, G4, -8, C5, 8, B4, -8, G4, 8, B4, -8, E5, 8,
		DS5, 1, D5, 2, REST, 4, REST, 8, DS4, 8, E4, -4, REST, 8, FS4, 8,
		G4, -4, REST, 8, DS4, 8, E4, -8, FS4, 8, G4, -8, C5, 8, B4, -8,
		E4, 8, G4, -8, B4, 8,
	     AS4, 2, A4, -16, G4, -16, E4, -16, D4, -16, E4, -4, REST, 4,
		REST, 4, E5, -8, D5, 8, B4, -8, A4, 8, G4, -8, E4, -8,
		AS4, 16, A4, -8, AS4, 16, A4, -8, AS4, 16, A4, -8, AS4, 16, A4, -8,
		G4, -16, E4, -16, D4, -16, E4, 16, E4, 16, E4, 2]


""" Song Function """
def PlaySong(pin, song):
    """
    Plays Songs
    ---If Threaded: Set ePLAYSONG to interrupt and end song
    """
    global ePLAYSONG
    global HW_PWM_DUTY
    
    print("Playing")
    for note in range(0, int(len(song)), 2):
        divisor = song[note+1]
        if (divisor > 0):
            beat_length = WHOLENOTE / divisor
        else:
            beat_length = WHOLENOTE / (-divisor)
            beat_length *= 1.5
        # The following time.sleep() allows for better interpretation of notes when played
        pi.hardware_PWM(pin, song[note], HW_PWM_DUTY)
        time.sleep(beat_length*0.9)
        pi.hardware_PWM(pin, REST, HW_PWM_DUTY)
        time.sleep(beat_length*0.1)
        
        if not ePLAYSONG.is_set():
            print("Done")
            break
