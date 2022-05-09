import time
import sys
import RPi.GPIO as GPIO

from threading import Thread, Lock, Event
from flask import Flask, render_template, redirect, request
from o_elec import *
from Notes import *
from Songs import *



"""=====_____Global Variables_____====="""
"""_____Flask_____"""
app = Flask(__name__, static_folder='assets')

"""_____Buzzer_____"""
BUZZ_PIN = 13
"""Tunes"""
DUTY = 500000   # 50% Duty Cycle provides best sound output
SONG = TETRIS   # Initial/Current Song
CURR_SONG = "Tetris"    # Initial/Current Song
TEMPO = 140     # Average Song Tempo ; Higher=Faster ; Lower=Slower
WHOLENOTE = (60 * 4) / TEMPO   # Time Length of Wholenote for Songs ; Helps determine beat lengths

"""_____LED Pins_____"""
LED_PIN = 6     # For Origami LEDs
# Physical UX Indicators
GREEN = 9   # GND ; Always Turns On
WHITE = 17  # LED
BLUE = 27   # Buzzer (+)
RED = 22      # Motor (+)
YELLOW = 10     # Motor (-)
LED_CON = [GREEN, WHITE, BLUE, RED, YELLOW] # All LEDs in a List

"""_____Motor_____"""
MOTOR_PIN = 12
M_FREQ = 50000    # PWM Freq = 50KHz
M_LEVEL = 3     # Vibration Level (1-5) ; Starts at Level 3 (Mid-Level)

"""_____Switches_____"""
START = 24      # Green Button
STOP = 25       # Red Button
BIRD= 14       # Blue Button
CROWN = 15      # White Button
HEAD = 23    # Yellow Button
BUTTONS = [25, 24, 14, 15, 23]  # Origami Selection Buttons 

"""_____Thread_____"""
# Event Variables
eBUZZER_RUN = Event()
eBUZZER_CONTROL = Event()
eMOTOR_CONTROL = Event()
eBIRD = Event()
eCROWN = Event()
eHEAD = Event()
eSELECTING = Event()
eREADY = Event()

# Lock Variables
lSELECT = Lock()

# Status Variables
# True=ON ; False=OFF
sCOMP = [True, True, True]       # Buzzer ; Motor ; LED 
sORIGAMI = [False, False, False]    # Bird ; Crown ; Head


"""=====_____Functions_____====="""
def Setup():
    global eSELECTING
    global BUZZ_PIN
    global MOTOR_PIN
    global LED_PIN
    global LED_CON
    global BUTTONS

    SetupHW_PWM(BUZZ_PIN, MOTOR_PIN)
    SetupOutput(LED_PIN, *LED_CON)
    SetupInput(*BUTTONS)

    eSELECTING.set()
    return

"""_____Main Selection Function_____"""
def WaitSelect():
    # Wait for Origami Creation Selection
    global BIRD
    global CROWN
    global HEAD
    global eREADY
    global eSELECTING
    global lSELECT
    global BUTTONS

    while True:
        eSELECTING.wait()
        with lSELECT:
            if ReadInputAll(*BUTTONS):
                eREADY.set()
                if ReadInput(BIRD):
                    SelectBird()
                elif ReadInput(CROWN):
                    SelectCrown()
                elif ReadInput(HEAD):
                    SelectHead()
                eREADY.set()          
"""Child Selection Functions"""
def SelectBird():
    global LED_CON
    global sORIGAMI
    global sCOMP

    for state in range(len(sCOMP)):
        if sCOMP[state]:
            ChangeOutput(LED_CON[0], 1)
            if state == 0:
                ChangeOutput(LED_CON[2], 1)
            elif state == 1:
                ChangeOutputAll(LED_CON[3:5], [1, 1])
            elif state == 2:
                ChangeOutput(LED_CON[1], 1)
        else:
            if state == 0:
                ChangeOutput(LED_CON[2], 0)
            elif state == 1:
                ChangeOutputAll(LED_CON[3:5], [0, 0])
            elif state == 2:
                ChangeOutput(LED_CON[1], 0)        

    for creation in range(len(sORIGAMI)):
        if creation == 0:
            sORIGAMI[creation] = True
        else:
            sORIGAMI[creation] = False
def SelectCrown():
    global LED_CON
    global sORIGAMI
    global sCOMP

    ChangeOutputAll(LED_CON[2:], [0]*3)
    if sCOMP[2]:
        ChangeOutputAll(LED_CON[0:2], [1]*2)
    else:
        ChangeOutputAll(LED_CON[0:2], [0]*2)

    for creation in range(len(sORIGAMI)):
        if (creation == 1):
            sORIGAMI[creation] = True
        else:
            sORIGAMI[creation] = False
def SelectHead():
    global LED_CON
    global sORIGAMI
    global sCOMP

    ChangeOutput(LED_CON[3:5], [0]*2)
    for state in range(0, len(sCOMP), 2):
        if sCOMP[state]:
            ChangeOutput(LED_CON[0], 1)
            if state == 0:
                ChangeOutput(LED_CON[2], 1)
            elif state == 2:
                ChangeOutput(LED_CON[1], 1)

    for creation in range(len(sORIGAMI)):
        if creation == 2:
            sORIGAMI[creation] = True
        else:
            sORIGAMI[creation] = False


"""_____Start/Running Functions_____"""
def StartStop():
    global eREADY
    global eSELECTING
    global eBIRD
    global eCROWN
    global eHEAD
    global sORIGAMI
    global START
    global STOP

    while True:
        eREADY.wait()
        
        if (eSELECTING.is_set()) & (ReadInput(START)):
            eSELECTING.clear()
            if sORIGAMI[0]:
                eBIRD.set()
            elif sORIGAMI[1]:
                eCROWN.set()
            elif sORIGAMI[2]:
                eHEAD.set()
        if (not eSELECTING.is_set()) & (ReadInput(STOP)):
            Reset()
"""Child Start/Stop Functions"""
def Reset():
    global eREADY
    global eSELECTING
    global eBUZZER_CONTROL
    global MOTOR_PIN
    global LED_PIN
    global DUTY
    global sORIGAMI
    global LED_CON
    eREADY.clear()
    eSELECTING.set()
    ePLAYSONG.clear()
    eBUZZER_CONTROL.clear()
    ChangeHW_PWM(REST, DUTY, MOTOR_PIN)
    ChangeOutput(LED_PIN, 0)

    ChangeOutputAll(LED_CON, [0]*5)
    for creation in sORIGAMI:
        creation = False
def RunBird():
    global LED_PIN
    global sCOMP
    global eBUZZER_CONTROL
    global eMOTOR_CONTROL
    global eBIRD

    while True:
        eBIRD.wait()
        if sCOMP[1]:
            eMOTOR_CONTROL.set()
        if sCOMP[0]:
            eBUZZER_CONTROL.set()
        if sCOMP[2]:
            ChangeOutput(LED_PIN, 1)
        eBIRD.clear()
def RunCrown():
    global sCOMP
    global eCROWN
    global LED_PIN

    while True:
        eCROWN.wait()
        if sCOMP[2]:
            ChangeOutput(LED_PIN, 1)
        eCROWN.clear()
def RunHead():
    global sCOMP
    global eBUZZER_CONTROL
    global LED_PIN
    global eHEAD

    while True:
        eHEAD.wait()
        if sCOMP[0]:
            eBUZZER_CONTROL.set()
        if sCOMP[2]:
            ChangeOutput(LED_PIN, 1)
        eHEAD.clear()

"""_____Component Functions_____"""
def Motor():
    global MOTOR_PIN
    global M_FREQ
    global eMOTOR_CONTROL
    while True:
        eMOTOR_CONTROL.wait()
        ChangeHW_PWM(M_FREQ, MotorDuty(), MOTOR_PIN)
        eMOTOR_CONTROL.clear()
def MotorDuty():
    global M_LEVEL
    return int(Map(M_LEVEL, 0, 5, 1000000, 250000))

def PlayTune():
    global BUZZ_PIN
    global SONG
    global eBUZZER_CONTROL
    global ePLAYSONG

    while True:
        eBUZZER_CONTROL.wait()
        ePLAYSONG.set()
        PlaySong(BUZZ_PIN, SONG)


"""______Flask Functions_____"""
@app.route("/")
def Home():
    return redirect("/templates/index")

@app.route("/templates/index")
def HomeTemplate():
    return render_template("index.html")

@app.route("/templates/origami")
def OrigamiTemplate():
    return render_template("origami.html")

@app.route("/templates/crow")
def CrowTemplate():
    return render_template("crow.html")

@app.route("/templates/crown")
def CrownTemplate():
    return render_template("crown.html")

@app.route("/templates/soprano")
def SopranoTemplate():
    return render_template("soprano.html")

@app.route("/templates/controls", methods=['POST','GET'])
def controls_template():
    global sCOMP

    Reset()

    if request.method=="POST":
        if request.form.get('VibState'):
            sCOMP[1] = True
        else:
            sCOMP[1] = False

        if request.form.get('SongState'):
            sCOMP[0] = True
        else:
            sCOMP[0] = False
        
        if request.form.get('LED'):
             sCOMP[2] = True
        else:
            sCOMP[2] = False

    return render_template("controls.html", VibState=sCOMP[1], SongState=sCOMP[0], LED=sCOMP[2], vib_levels=SetMotorVar(), songs=SetSongVar())
def SetSongVar():
    """
    Creates List[Dictionary] values for controls_template
    GET/POST: Sets appropriate values to show current song
    POST: Changes Song to be played
    """
    global SONG
    global CURR_SONG

    # Dictionary Values for Song Drop-down
    songs = [{"value": "Tetris", "song": "Tetris", "selected": False},
            {"value": "Pink", "song": "Pink Panther", "selected": False},
            {"value": "Birthday", "song": "Happy Birthday", "selected": False},
            {"value": "Canon", "song": "Canon in 'D' Minor", "selected": False}]

    # Gets value of Song
    song = request.form.get('Song') # None=GET ; Other=POST

    # Checks if Request was GET or POST
    # Sets appropriate Song value for Drop-down
    if not song:
        # GET Request
        for tune in songs:
            if (CURR_SONG == tune["value"]):
                tune["selected"] = True
            else:
                tune["selected"] = False           
    else:
        # POST Request
        # Sets song value according to given configuration
        for tune in range(len(songs)):
            if (songs[tune]["value"] == song):
                songs[tune]["selected"] = True
                CURR_SONG = song
                if tune == 0:
                    SONG = TETRIS
                elif tune == 1:
                    SONG = P_PANTHER
                elif tune == 2:
                    SONG = BIRTHDAY
                elif tune == 3:
                    SONG = CANON
            else:
                songs[tune]["selected"] = False
    return songs
def SetMotorVar():
    """
    Creates Dictionary Values for controls_template
    GET/POST: Sets appropriate Values to show current vibration level 
    POST: Changes Motor Level to submitted configurations
    """
    global M_LEVEL

    # Dictionary Values for Motor Intensity Drop-down
    vib_levels = [{"value": "1", "level": "Level 1", "selected": False},
            {"value": "2", "level": "Level 2", "selected": False},
            {"value": "3", "level": "Level 3", "selected": False},
            {"value": "4", "level": "Level 4", "selected": False},
            {"value": "5", "level": "Level 5", "selected": False}]
    
    # Gets value of Motor Intensity
    level_in = request.form.get('VibLevel') # None=GET ; Other=POST

    # Checks if Request was GET or POST
    # Selects appropriate Motor Intensity Drop-down
    if not level_in:
        # GET request
        for level in vib_levels:
            if str(-(M_LEVEL-6)) == level["value"]:
                level["selected"] = True
            else:
                level["selected"] = False
    else:
        # Post Request
        # Sets vibration level value according to given configuration
        for level in vib_levels:
            M_LEVEL = 6 - int(level_in)
            if level["value"] == level_in:
                level["selected"] = True
            else:
                level["selected"] = False
    return vib_levels

"""=====_____Main Code_____====="""
try:
    Setup()

    select = Thread(target=WaitSelect).start()
    start_stop = Thread(target=StartStop).start()
    motor = Thread(target=Motor).start()
    tunes = Thread(target=PlayTune).start()
    bird = Thread(target=RunBird).start()
    crown = Thread(target=RunCrown).start()
    head = Thread(target=RunHead).start()

    app.run(host='0.0.0.0', port=80, debug=False, threaded=True)

except KeyboardInterrupt:
    ResetGPIO()
    sys.exit()
