#!/bin/bash

trap "exit" INT TERM ERR
trap "kill 0" EXIT

source /opt/ros/kinetic/setup.bash
source /home/husarion/ros_workspace/devel/setup.sh

sudo sixad -s &
#roslaunch fox_bringup fox.launch &
roslaunch teleop_twist_joy_fox teleop_fox.launch &

wait
