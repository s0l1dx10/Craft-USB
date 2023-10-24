#!/bin/bash

LED GREEN FAST

SYNC_PAYLOADS # Make sure the payloads folder is in the usb-storage device that the target gets
ATTACKMODE STORAGE HID # Setup the gadgets so the PI presents itself as a HID and a storage device

keyboardLayout="US"
export keyboardLayout # I needed my own keyboard layout defined in duckpi.sh

QUACK DELAY 1000
QUACK GUI r
QUACK DELAY 100
QUACK STRING "notepad.exe"
QUACK ENTER
QUACK DELAY 1000
QUACK STRING "You have been hacked Mohammad Abdulfattah"

# Now we keep looking on the storage device if the target finished. We set a timeout of 120 seconds
WAIT_TARGET 120
exitCode=$?
if [ $exitCode -eq 0 ]; then
	# The target has written a file called target_finished in the root of the storage device. We are happy!
	LED RED OFF
	LED GREEN ON
else
	# We never heard from the target. Something went wrong!
	LED GREEN OFF
	LED RED FAST
fi
