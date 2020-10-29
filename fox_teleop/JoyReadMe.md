## Steps to use ps3 joystick to send cmd_vel

- run ps3joy.py script (in the ps3joy package provided. The script in the provided package consists of some changes to ensure js0 is the device and the mouse output is ignored)

- run the teleop_joy.launch.xml file. This launches a joy_node that takes the ps3joy input and publishes to /joy and then launches the script teleop_joy.py to convert to cmd_vel. Edit this last script if required to publish to another topic.