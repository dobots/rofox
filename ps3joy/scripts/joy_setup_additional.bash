#!/bin/bash

# Disable mouse input from joystick
ps3_id=$(xinput -list | grep "Sony Playstation SixAxis/DS3" | awk '{print $6}' | cut -d'=' -f2)
xinput --disable $ps3_id

# Rename joy to js0 (in case it is js1)
sudo mv /dev/input/js1 /dev/input/js0

# Give all users rw permissions
sudo chmod a+rw /dev/input/js0
