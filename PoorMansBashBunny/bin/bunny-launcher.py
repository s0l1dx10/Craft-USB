
import rpyc
import time
import threading
import RPi.GPIO as GPIO
from subprocess import Popen
from rpyc.utils.server import ThreadedServer
import os
import logging 

logging.basicConfig(level="INFO")

##############################################Definitions#


PAYLOAD_DIR = "/bunny/payloads"

# Listen on port for LED commands
TCP_PORT = 18861

# IO port definitions




IO_LEDS = {"green":19, "red":11} # green on gpio 19. etc

IO_DIP = [2, 3, 4, 17] # Dip switch1 on io pin2, switch2 on io pin3 etc.
# -------------------------- Globals ------------------------

ledModes = {} # list of all leds and their current status (off, slow, fast, on)
# ledModes = {"LED1": "off", "LED2": "slow", "LED3": "high"}

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




# Background thread that takes care of the leds and checks the buttons   ###BACK here
# This runs forever.
def bgHandler():
    global IO_LEDS, ledModes
    blinkCounter = 0 # Is used for timing the leds blinking frequency
    while True:
        blinkCounter += 1
        for ledName, ledPin in IO_LEDS.items(): # Go through each led in the led-list
            if ledModes.get(ledName) == "off": GPIO.output(IO_LEDS[ledName], False )
            if ledModes.get(ledName) == "slow": GPIO.output(IO_LEDS[ledName], blinkCounter % 16 < 8 ) # Using modulus to define frequency
            if ledModes.get(ledName) == "fast": GPIO.output(IO_LEDS[ledName], blinkCounter % 4 < 2 )
            if ledModes.get(ledName) == "on": GPIO.output(IO_LEDS[ledName], True )

time.sleep(0.1) # Keep the cpu from melting - it also defines the max blink frequency
###################################
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


# Handles incoming socket connections to control the leds
class ledService(rpyc.Service):
    def on_connect(self, conn): # Do nothing when somebody connects
        pass

    def on_disconnect(self, conn): # Do nothing when somebody disconnects
        pass

    def exposed_blink(self, ledName, ledMode): # We expect a ledname and a blinking mode for it
        global ledModes
        ledModes[ledName.lower()] = ledMode.lower() # We set it globally so that our bgHandler can do the blinking
        logging.info("Setting led {} to {}".format(ledName, ledMode))
        return True 


# -------------------------- Main ------------------------

if __name__ == "__main__":
    setupIO()
    runBootScript()

    # Start the background handler for the leds and buttons
    bgHandler_thread=threading.Thread(target=bgHandler)
    bgHandler_thread.start() 

    # Start listening on a tcpport for commands. The commands are handled by ledService
    t = ThreadedServer(ledService, port=TCP_PORT)
    t.start() 