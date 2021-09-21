# Hardware-in-the-loop (HIL) simulation 

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

# Startup instructions

1. In 2 terminals ssh to the robot:
```
ssh husarion@192.168.8.124
```

2. Start roscore on the robot:
```
roscore
```

3. Start Gazebo and RViz simulation on the laptop:
```
roslaunch fox_hil_sim fox_hil_gazebo.launch rviz:=true
```

4. Start serial node on the robot:
```
roslaunch fox_bringup fox.launch
```

It is important to start first the simulation and then the rosserial bridge within the fox.launch! Otherwise, RViz will complain about old laserscan data and it will not be shown in RViz.

5. Start teleop on the laptop:
```
rosrun teleop_twist_keyboard teleop_twist_keyboard.py 
```
## Troubleshooting

### Only one wheel moves
- try unplugging and replugging the batteries
- charge the batteries
- reconfigure the wheels with the VESC tool (use instruction video on github.com/dobots/core2_firmware/docs_and_specs
- flash the CORE2 firmware ( use the ready firmware from github.com/dobots/core2_firmware/fox-firmware/ready_firmware and follow the instructions at github.com/dobots/core2_firmware/fox-firmware from the "Upload firmware" section) - you only need to copy it to the right folder at the robot and then running it with the stm32 loader.

## Notes:
- fox.launch file starts the serial communication between the CORE2 board and the tinker board. In addition it starts the ekf_localization package. 
- ekf-localization is needed for two purposes: 
	- 1. fuses the odometry data and the imu data.
	- 2. creates and odom frame - which is needed to have a fixed frame for RViz
- fox_hil_gazebo.launch starts Gazebo, RViz, spawns the model and the gazebo_model_update.py script. 
- gazebo_model_update.py script subscribes to the /pose message from the robot and publishes it to the gazebo/set_model_state topic. It can be configured to subscribe to the filtered odometry data from the ekf package as well. ( Unfortunately, the IMU is rotated by 180 degrees in the robot, so we need to edit the CORE2 firmware. The current solution is to unplug the IMU at the robot and subscribe to the raw /pose message)



