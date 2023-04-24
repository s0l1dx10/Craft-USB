# This should be called with one parameter: The timeout. How long time we are going to wait for the target.
# If target has written a file called "target_finished" in the root of the storage device we return exit code 0.
# If we don't hear from target withing the timeout time, we return exit code 1.
#timeout mechanism using a while loop to repeatedly check for the existence of a file named by the "WAIT_FILE" variable within a mounted file system. If the file is found within the specified timeout duration, the script exits with a status code of 0, indicating success. If the timeout expires and the file is not found, the script exits with a status code of 1, indicating failure.
BUNNY_DIR="/bunny"
WAIT_FILE="target_finished"
#ets up a variable "BUNNY_DIR" with the value "/bunny", and another variable "WAIT_FILE" with the value "target_finished". It also initializes variables for "timeout", "startTime", and "currentTime".

timeout=$1 
#This line assigns the value of the first argument passed to the script (referred to as "$1") to the variable "timeout". This allows the script to accept a timeout value as an argument when it is executed.
startTime=$(date +%s)
#This line uses the "date" command to get the current timestamp in seconds since the epoch (January 1, 1970) using the "+%s" format option, and assigns it to the "startTime" variable. This serves as the starting time for measuring the timeout duration.
currentTime=$startTime
#This line assigns the value of "startTime" to the "currentTime" variable, initializing it with the same value as "startTime".
while [ `expr $currentTime - $startTime` -lt $timeout ]; do # If we have not timed out
#This line starts a while loop that continues as long as the difference between the "currentTime" and "startTime" is less than the "timeout" value provided as an argument
	currentTime=$(date +%s)
    #This line updates the "currentTime" variable with the current timestamp in seconds since the epoch, allowing the script to track the elapsed time.
	umount $BUNNY_DIR/storage/system.img
    #This line unmounts the file system located at "$BUNNY_DIR/storage/system.img"
	mount -o ro $BUNNY_DIR/storage/system.img $BUNNY_DIR/mnt # Mount the storage imgage
    #This line mounts the file system located at "$BUNNY_DIR/storage/system.img" to the directory "$BUNNY_DIR/mnt" in read-only mode, allowing the script to access the contents of the file system.
	if [ -f $BUNNY_DIR/mnt/$WAIT_FILE ]; then # If we found our file we return with happiness (0)
    #This line checks if the file "$WAIT_FILE" exists within the mounted file system, using the "-f" test flag to check for regular files. If the file is found, the script exits with a status code of 0 using the "exit" command, indicating success.
		exit 0
	fi
	sleep 1
    #This line pauses the script for 1 second, allowing a delay between iterations of the while loop.
done
exit 1 # We have timed out and we are sad (1)
# If the while loop completes without finding the "$WAIT_FILE" within the timeout duration, the script exits with a status code of 1 using the "exit" command, indicating failure.
# finally we cheack the code to give me the target file that I chose to cheack the code success or not 
