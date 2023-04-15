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


