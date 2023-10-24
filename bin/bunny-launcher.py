#!/usr/bin/env python

import rpyc
import time
import threading
import RPi.GPIO as GPIO
from subprocess import Popen
from rpyc.utils.server import ThreadedServer
import os
import logging

logging.basicConfig(level="INFO")



# -------------------------- Definitions ------------------------

PAYLOAD_DIR = "/bunny/payloads"

# Listen on port for LED commands
TCP_PORT = 18861

# IO port definitions

IO_RED 		= 2	# red gpio 5
IO_GREEN 	= 3	# green gpio 11
IO_BLUE 	= 4	# blue gpio 9

IO_LEDS = {"green": IO_GREEN, "red": IO_RED, "blue": IO_BLUE} # mapping base colors to pins
IO_DIP = [26, 19, 13, 6] # Dip switch1 on io pin2, switch2 on io pin3 etc.
IO_BUTTONS = {"green":13, "red":19} # green button on io 13 etc


# -------------------------- Globals ------------------------

ledModes = {} # list of all leds
mode = "off"  # and their current status (off, slow, high, on)



# -------------------------- Functions ------------------------

# Sets up all IO pins for DIP switches, LEDs and buttons.
def setupIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Initialize leds
    global IO_LEDS, ledModes
    for ledName,ledPin in IO_LEDS.items():
        ledModes[ledName] = "off"
        GPIO.setup(ledPin, GPIO.OUT)
    # Dip Switches as pulled up inputs
    for dipPin in IO_DIP:
        GPIO.setup(dipPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Buttons as pulled up imputs
    for buttonName, buttonPin in IO_BUTTONS.items():
        GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    logging.info("IO setup completed")



# Background thread that takes care of the leds and checks the buttons
# This runs forever.
def bgHandler():
    global IO_LEDS, ledModes
    blinkCounter = 0 # Is used for timing the leds blinking frequency
    colorModes = {
	"slow", "fast", "veryfast",	# blink (on_time = off_time)
	"on", "solid",			# 100% on time
	"single", "double", "triple", "quad", "quin",	# blink n times very short and wait one second
	"isingle", "idouble", "itriple", "iquad", "iquin"} # inverse blink n times very short and wait one second
    currentMode = ""
    while True:
	colorValues = {"red": False, "green": False, "blue": False}	# reset current color profile
	previousMode = currentMode
	currentMode = "off"	# reset current mode
        for ledName, ledPin in IO_LEDS.items(): # Go through each led in the led-list
            if ledModes.get(ledName) in colorModes:	# only process active leds
		colorValues[ledName] = True		# set led color true
		currentMode = ledModes.get(ledName)	# and rememver the currend mode. 
							# ToDo: this is horse shit:
							# there is only one mode. not one mode for each led
	if currentMode != previousMode:
            blinkCounter = 0
        else:
            blinkCounter += 1

	if currentMode == "on" or currentMode == "solid":
	    LEDOn(colorValues["red"], colorValues["green"], colorValues["blue"])
	elif currentMode == "slow":
            LEDBlink(colorValues["red"], colorValues["green"], colorValues["blue"], 200, 100, blinkCounter)
	elif currentMode == "fast":
	    LEDBlink(colorValues["red"], colorValues["green"], colorValues["blue"], 20, 10, blinkCounter)
	elif currentMode == "veryfast":
            LEDBlink(colorValues["red"], colorValues["green"], colorValues["blue"], 10, 5, blinkCounter)
	elif currentMode == "single":
	    LEDBlinkN(colorValues["red"], colorValues["green"], colorValues["blue"], 1, blinkCounter)
	elif currentMode == "double":
            LEDBlinkN(colorValues["red"], colorValues["green"], colorValues["blue"], 2, blinkCounter)
        elif currentMode == "triple":
            LEDBlinkN(colorValues["red"], colorValues["green"], colorValues["blue"], 3, blinkCounter)
        elif currentMode == "quad":
            LEDBlinkN(colorValues["red"], colorValues["green"], colorValues["blue"], 4, blinkCounter)
        elif currentMode == "quin":
            LEDBlinkN(colorValues["red"], colorValues["green"], colorValues["blue"], 5, blinkCounter)
        elif currentMode == "isingle":
            LEDBlinkInvN(colorValues["red"], colorValues["green"], colorValues["blue"], 1, blinkCounter)
        elif currentMode == "idouble":
            LEDBlinkInvN(colorValues["red"], colorValues["green"], colorValues["blue"], 2, blinkCounter)
        elif currentMode == "itriple":
            LEDBlinkInvN(colorValues["red"], colorValues["green"], colorValues["blue"], 3, blinkCounter)
        elif currentMode == "iquad":
            LEDBlinkInvN(colorValues["red"], colorValues["green"], colorValues["blue"], 4, blinkCounter)
        elif currentMode == "iquin":
            LEDBlinkInvN(colorValues["red"], colorValues["green"], colorValues["blue"], 5, blinkCounter)
	else:
	    LEDOff()
        handleButtons() # Check and handle if anyone pressed a button
	time.sleep(0.01)

# Blink n times very short and wait.
# Is used to show the current stage
# this might cause a long loop and no reactions to buttons.
# ToDo: find a better solution.
def LEDBlinkN(red, green, blue, n, blinkCounter):
    if blinkCounter % 100 == 0:
    	for i in range(n):
		LEDOn(red, green, blue)
		time.sleep(0.075)
		LEDOff()
		time.sleep(0.075)

# Be solid with n very short off-blinks
# ToDo: find a better solution
def LEDBlinkInvN(red, green, blue, n, blinkCounter):
    if blinkCounter % 100 == 0:
    	for i in range(n):
            LEDOff()
            time.sleep(0.075)
            LEDOn(red, green, blue)
            time.sleep(0.075)

# Blink the LED.
# Color is defined by booleans for red, green and blue.
# - intervall defines the length of one completion
# - on_time defines the active time of the led during one intervall
# - blink counter tells the function on what position of the intervall we are
def LEDBlink(red, green, blue, intervall, on_time, blinkCounter):
    if blinkCounter % intervall < on_time:
	LEDOn(red, green, blue)
    else:
	LEDOff()

# Turn LED on.
# Color is defined by booleans for red, green and blue.
def LEDOn(red, green, blue):
    global IO_LEDS
    GPIO.output(IO_LEDS["red"], red)
    GPIO.output(IO_LEDS["green"], green)
    GPIO.output(IO_LEDS["blue"], blue)

# Turn LED off
def LEDOff():
    LEDOn(False, False, False)

# Goes through the list of buttons and checks if any is pressed. If pressed it looks at the DIP switches
# and launches the matching shell script. example:
# Green button is pressed while dip switches are set to 0110, then "/bunny/payloads/6/button_green" is launched
def handleButtons():
    for buttonName, buttonPin in IO_BUTTONS.items(): # Traverse all buttons defined in the list
        if not GPIO.input(buttonPin): # Button pressed 
           logging.info ("{} button pressed.".format(buttonName))
           launchFile = PAYLOAD_DIR + "/" + str(getSwitch()) + "/button_" + buttonName 
           if os.path.exists(launchFile): # The file exists
               logging.info("Launching script at: {0}".format(launchFile))
               Popen(launchFile) # We launch it in the background
               time.sleep(0.3) # Avoid key bouncing
           else: # File didn't exist
               logging.info("No script file at: {0}".format(launchFile))



# Returns decimal reprecentation of the DIP switches. Eg: Switches set to 1001, returns 9
def getSwitch():
    value = 15 - ( GPIO.input(IO_DIP[0])*1 + GPIO.input(IO_DIP[1])*2 +  GPIO.input(IO_DIP[2])*4 + GPIO.input(IO_DIP[3])*8 )
    return value



# This is called when this program is run. It looks at the DIP switches and launches a shell script
# according to the setting. Eg: dip switches set to 1000 a script at "/bunny/payloads/8/boot" is called
def runBootScript():
    switch = getSwitch()
    launchFile = PAYLOAD_DIR + "/" + str(switch) + "/boot"
    logging.info("DIP Switch : {0}".format(switch))

    if os.path.exists(launchFile): # The file exists
        logging.info("Launching boot script at: {0}".format(launchFile))
        Popen(launchFile) # Launch it in the background
    else:
        logging.info("No boot script file at: {0}".format(launchFile))



# -------------------------- Classes ------------------------

# Handles incoming socket connections to control the leds
class ledService(rpyc.Service):
    def on_connect(self, conn): # Do nothing when somebody connects
        pass

    def on_disconnect(self, conn): # Do nothing when somebody disconnects
        pass

    def exposed_blink(self, ledName, ledMode): # We expect a ledname and a blinking mode for it
        global ledModes
	allColors = set(ledModes.keys())
	# rgb led
        colorMix = {
            "r": {"red"},                   # red
	    "red": {"red"},
            "g": {"green"},                 # green
	    "green": {"green"},
            "b": {"blue"},                  # blue
	    "blue": {"blue"},
            "y": {"red", "green"},          # yellow
	    "yellow": {"red", "green"},
            "c": {"green", "blue"},         # cyan (light blue)
	    "cyan": {"green", "blue"},
            "m": {"red", "blue"},           # magenta (violet / purple)
	    "magenta": {"red", "blue"},
            "w": {"red", "green", "blue"},  # white
	    "white": {"red", "green", "blue"},
	    "black": {},
	    # color shortcuts
	    "setup": {"red", "blue"},
	    "fail": {"red"},
	    "finish": {"green"},
	    "stage": {"red", "green"},
	    "special": {"green", "blue"},
	    "cleanup": {"red", "green", "blue"}
            }
	shortcuts = {
	    # key: shortcut name
	    # value: pair of color and mode

	    # init
	    "setup": 	("m", "solid"),
	    # fails
	    "fail": 	("r", "slow"),
            "fail1":    ("r", "slow"),
            "fail2":    ("r", "fast"),
            "fail3":    ("r", "veryfast"),
	    # attack
	    "attack":	("y", "single"),
	    "stage1":   ("y", "single"),
            "stage2":   ("y", "double"),
            "stage3":   ("y", "triple"),
            "stage4":   ("y", "quad"),
            "stage5":   ("y", "quin"),
	    # special
	    "special":	("c", "isingle"),
            "special1": ("c", "isingle"),
            "special2": ("c", "idouble"),
            "special3": ("c", "itriple"),
            "special4": ("c", "iquad"),
            "special5": ("c", "iquin"),
	    # cleanup
	    "cleanup":	("w", "fast"),
	    # finish
	    "finish":	("g", "solid"),
	    # off
	    "off":	("b", "off")
	    }
	if ledName == None:
            ledName, ledMode = shortcuts[ledMode.lower()]
	ledColor = colorMix[ledName.lower()]
	for led in ledColor:
            ledModes[led] = ledMode.lower()
	ledOff = allColors.difference(ledColor)
	for led in ledOff:
	    ledModes[led] = "off"
        logging.info("Setting led {} to {}".format(ledName, ledMode))
        return True



# -------------------------- Main ------------------------

if __name__ == "__main__":
    setupIO()
    runBootScript()

    # Start the background handler for the leds and buttons
    bgHandler_thread=threading.Thread(target=bgHandler)
    bgHandler_thread.start()

    # Start listening on a tcp port for commands. The commands are handled by ledService
    t = ThreadedServer(ledService, port=TCP_PORT)
    t.start()