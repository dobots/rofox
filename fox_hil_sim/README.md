# Hardware-in-the-loop simulation 

This package contains  ros packages for running the HIL simulation example using the rover.
It is designed for overiding the position of the simulated robot in Gazebo. It collects the position of the real robot (/pose topic for hFramework) and publishes this position on gazebo/set_model_state position. (The simulated robot in Gazebo must be configured to not listen to /cmd_vel topic. This is done by introducing /cmd_vel2 in /rosbot_description/src/rosbot_description/src/urdf/hil_rosbot.gazebo and .xacro)

## Instructions 

1. Create a hil_ws on your local machine:
 ```
source /opt/ros/melodic/setup.bash
mkdir -p ~/hil_ws/src
cd ~/hil_ws/
catkin_make
 ```

2. Create a simlink to the rofox folder  in your src folder of your catkin workspace: 
```
ln -s ~/<your_github_folder>/rofox/ ~/hil_ws/src
```

3.  Build these packages:
```
catkin_make
```
4. Source the environment:
```
source ~/hil_ws/devel/setup.bash
```

# Setup connection between robot and your laptop

1. Ssh to the robot:
```
ssh husarion@<ip-adress-of-the-robot>
```
If you don't know the IP adress of the robot, then connect to it with a keyboard and a screen and in a terminal run `ifconfig`

2. Edit the ~/.bashrc file of the robot to set it to be the ros master:
```
export ROS_MASTER_URI=http://<ip-adress-of-the-robot>:11311/
export ROS_IP=<ip-adress-of-the-robot>
```
3. Source it:
```
 source ~/.bashrc 
 ```

4. Open the `~/.bashrc` file on your laptop and configure the same parameters. Pay attention, that now you need to fill in the IP adress of the robot as master IP adress and your own ip adress in the ros_ip line:
```
export ROS_MASTER_URI=http://<ip-adress-of-the-robot>:11311/
export ROS_IP=<your-ip-adress>
```

5. Source it:
```
 source ~/.bashrc 
 ```

# Startup instructions

1. In two terminals ssh to the robot:
```
ssh husarion@<ip-adress-of-the-robot>
```

2. Start roscore on the robot:
```
roscore
```

3. Start Gazebo and RViz simulation on the laptop:
```
roslaunch fox_hil_sim fox_hil_gazebo.launch rviz:=true
```
- fox_hil_gazebo.launch starts Gazebo, RViz, spawns the model and the gazebo_model_update.py script. 
- **gazebo_model_update.py** script subscribes to the /pose message from the robot and publishes it to the gazebo/set_model_state topic. It can be configured to subscribe to the filtered odometry data from the ekf package as well. ( Unfortunately, the IMU is rotated by 180 degrees in the robot, so we need to edit the CORE2 firmware. The current solution is to unplug the IMU at the robot and subscribe to the raw /pose message)

4. Start serial node on the robot:
```
roslaunch fox_bringup fox.launch
```
- fox.launch file starts the serial communication between the CORE2 board and the tinker board. In addition it starts the ekf_localization package. 
- ekf-localization is needed for two purposes: 
	- 1. fuses the odometry data and the imu data.
	- 2. creates and odom frame - which is needed to have a fixed frame for RViz

**It is important to start first the simulation and then the rosserial bridge within the fox.launch! Otherwise, RViz will complain about old laserscan data and it will not be shown in RViz.**

5. Start teleop on the laptop or start the joystick:
```
rosrun teleop_twist_keyboard teleop_twist_keyboard.py 
```
or
```
rosrun joy joy_node
rosrun teleop_twist_joy leop_node 
```


## Troubleshooting

### Only one wheel moves
- try unplugging and replugging the batteries
- charge the batteries
- reconfigure the wheels with the VESC tool (use instruction video on github.com/dobots/core2_firmware/docs_and_specs
- flash the CORE2 firmware ( use the ready firmware from github.com/dobots/core2_firmware/fox-firmware/ready_firmware and follow the instructions at github.com/dobots/core2_firmware/fox-firmware from the "Upload firmware" section) - you only need to copy it to the right folder at the robot and then running it with the stm32 loader.

### The robot shakes in the simulation
- try lower the ground plane in Gazebo, it might be conflicting with the z axis of the robot. The position of the real robot is z=0, while the simulated robots position is z=0.1, when it is on the ground. Now the simulated robot is spawned at the position of the real robot so it is important to lower the simulated ground.

##The joystick is not connected through bluetooth
-try to connect the joystick to the laptop instead of the robot
-try to use the built-in bluetooth instead of an external bluetooth dongle
-turn on the bluetooth receiver of your laptop and turn on the joystick
-in the settings of Ubuntu select the joystick device and connect
-useful commands for debugging:
	-to get the list of input device use: `ls /dev/input`
	-test the input of the joystick: `sudo jstest /dev/input/jsX`
	-make sure that it is accesible for the ROS joy node: `ls -l /dev/input/jsX` 
	- if not modify the read and write rights: `sudo chmod a+rw /dev/input/jsX`
-if the joystick is not on js0, you need to modify the parameter of the joy_node: `rosparam set joy_node/dev "/dev/input/jsX". Then you can start the joy_node and the teleop.
