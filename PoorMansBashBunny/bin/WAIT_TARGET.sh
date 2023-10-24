#!/bin/bash

# This should be called with one parameter: The timeout. How long time we are going to wait for the target.
# If target has written a file called "target_finished" in the root of the storage device we return exit code 0.
# If we don't hear from target withing the timeout time, we return exit code 1.

BUNNY_DIR="/bunny"
WAIT_FILE="target_finished"

timeout=$1
startTime=$(date +%s)
currentTime=$startTime

while [ `expr $currentTime - $startTime` -lt $timeout ]; do # If we have not timed out
	currentTime=$(date +%s)
	umount $BUNNY_DIR/storage/system.img
	mount -o ro $BUNNY_DIR/storage/system.img $BUNNY_DIR/mnt # Mount the storage imgage
	if [ -f $BUNNY_DIR/mnt/$WAIT_FILE ]; then # If we found our file we return with happiness (0)
		exit 0
	fi
	sleep 1
done
exit 1 # We have timed out and we are sad (1)