#!/usr/bin/python

# this should be called with two parameters.
# 1) the name of the led (RED or GREEN).
# 2) the mode (OFF, SLOW, FAST, ON)

import rpyc
import sys

led=sys.argv[1]
mode=sys.argv[2]
c = rpyc.connect("localhost", 18861) # The local port for IPC with the bunny-launcher
c.root.blink(led, mode)