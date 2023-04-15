#import part 
import rpyc #remote python call
import time #worke with time values
import threading #worke with threads in multi_threaded envirnment
import RPi.GPIO as GPIO #for controlling raspberry pi'sgeneral purpose input output pins
from subprocess import Popen #allow to execute shell command 
from rpyc.utils.server import ThreadedServer #provide simple way to create a multi_threaded RPC server that can handle multiable clint connection
import os # provide a way to interaction with the operation system
import logging # log messsage 

logging.basicConfig(level="INFO")
 
#Definitions part
PAYLOAD_DIR = "/bunny/payloads"
TCP_PORT =??
IO_LEDS = {} 
IO_DIP = [] 

 #globale part 
ledModes = {} # store mapping between LED modes and thire crospondeing value

# Functions part

def setupIO(): #get the function of the setup input and output pins
    GPIO.setmode(GPIO.BCM) # get the GPIO liberary to use BCM numbering schame 
    GPIO.setwarnings(False) #turn off warning 
    # Initialize leds
    global IO_LEDS, ledModes # decleare the globale variable IO_LED, ledMode
    for ledName,ledPin in IO_LEDS.items(): # dictinary for two maps LED name to GPIO and current mode and go to item to take led name and no of bin
        ledModes[ledName] = "off" #state the intial mode of LED  
        GPIO.setup(ledPin, GPIO.OUT) # connect the out by the state of LED
    # Dip Switches as pulled up inputs
    for dipPin in IO_DIP: #read the state of pin, which is usful for detecting when dip switch is turned on, of
        GPIO.setup(dipPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # know the level of intial pullup resistor. level(1) or level(0)
logging.info("IO setup completed") 

#set the state of led 

def bgHandler():
    global IO_LEDS, ledModes
    blinkCounter = 0 # Is used for timing the leds blinking frequency
    while True:
        blinkCounter += 1
        for ledName, ledPin in IO_LEDS.items(): # Go through each led in the led-list
            if ledModes.get(ledName) == "off": GPIO.output(IO_LEDS[ledName], False )
            if ledModes.get(ledName) == "slow": GPIO.output(IO_LEDS[ledName], blinkCounter % ? <?  ) 
            if ledModes.get(ledName) == "fast": GPIO.output(IO_LEDS[ledName], blinkCounter % ? <?   )
            if ledModes.get(ledName) == "on": GPIO.output(IO_LEDS[ledName], True )
time.sleep(0.1) # to save the CPU from damage

#switch setup
def getSwitch():
    value = 15 - ( GPIO.input(IO_DIP[0])*1 + GPIO.input(IO_DIP[1])*2 +  GPIO.input(IO_DIP[2])*4 + GPIO.input(IO_DIP[3])*8 )
    return value

# This is called when this program is run. It looks at the DIP switches and launches a shell script
def runBootScript(): # function reterieves the value of Dip switch using the (get switch()) function and stores it in the switch variable
    switch = getSwitch()
    launchFile = PAYLOAD_DIR + "/" + str(switch) + "/boot" # make a file path for the boot script
    logging.info("DIP Switch : {0}".format(switch)) #message include the value of switch which presumably represents the currnt setting of DIPswitch the message formated using str.format methode 

    if os.path.exists(launchFile): # The file exists
        logging.info("Launching boot script at: {0}".format(launchFile))
        Popen(launchFile) # Launch it in the background
    else:
        logging.info("No boot script file at: {0}".format(launchFile)) #no boot scrit file was found

#Classes part
 
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
#main part
if __name__ == "__main__":
    setupIO() #to connect input and output by the script
    runBootScript() 
#you can use it when the device is first powered or program started
# Start the background handler for the leds and buttons
    bgHandler_thread=threading.Thread(target=bgHandler)
    bgHandler_thread.start() 
 # Start listening on a tcpport for commands. The commands are handled by ledService
    t = ThreadedServer(ledService, port=TCP_PORT)
    t.start() 


