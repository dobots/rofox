# rofox packages

This repository contains the ROS packages for the RoFox robot by DoBots.
You may choose the branch as per your ROS distribution (This is the **ros2-eloquent** branch).

The **Migration_to_ROS2.md** file contains information on how to port your packages from ROS1 to ROS2.

Below you can find instructions on how to bringup the Gazebo simulation, run SLAM algorithms, localization or autonomous navigation.

## Source your workspace
```
source <workspace_path>/install/local_setup.bash
```

## Start the simulation with teleop

To launch the arena:
```
ros2 launch fox_bringup fox_gazebo.launch.xml
```
To start the keyboard teleop:

```
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

To run RViz:
```
rviz2
```

## Start SLAM (using cartographer)
```
#1. Simulation
ros2 launch fox_bringup fox_gazebo.launch.xml

#2. Teleoperation
ros2 run teleop_twist_keyboard teleop_twist_keyboard

#3. SLAM (Cartographer)
ros2 launch fox_localization cartographer.launch.xml

#4. RViz
rviz2
```

## Start AMCL
```
#1. Simulation
ros2 launch fox_bringup fox_gazebo.launch.xml

#2. Teleoperation
ros2 run teleop_twist_keyboard teleop_twist_keyboard

#3. AMCL
ros2 launch fox_localization amcl.launch.xml

#4. RViz
rviz2
```

## Start autonomous navigation (Nav2) with Cartographer
```
#1. Simulation
ros2 launch fox_bringup fox_gazebo.launch.xml

#2. Teleoperation
ros2 run teleop_twist_keyboard teleop_twist_keyboard

#3. SLAM (Cartographer)
ros2 launch fox_localization cartographer.launch.xml

#4. RViz
rviz2

#5. Navigation
ros2 launch fox_navigation navigation2.launch.xml 
```

## Start autonomous navigation (Nav2) with AMCL
```
#1. Simulation
ros2 launch fox_bringup fox_gazebo.launch.xml

#2. Teleoperation
ros2 run teleop_twist_keyboard teleop_twist_keyboard

#3. AMCL
ros2 launch fox_localization amcl.launch.xml

#4. RViz
rviz2

#5. Navigation
ros2 launch fox_navigation navigation2.launch.xml 
```

### Notes:

- Clone rplidar_ros (https://github.com/allenh1/rplidar_ros) to launch the rplidar hardware.

### ToDo:

- rosserial.launch.xml needs to be ported to ROS2. (Possibilities could be: https://github.com/husarion/rosbot-firmware-ros2 or https://github.com/osrf/ros2_serial_example)

- fox_ekf needs to be ported to ROS2. Based on the robot firmware, the pose message conversion may or may not be needed.

- ROS2 version of astra_launch package still needed for camera.launch.xml.xml

- joystick fox needs to be ported (if required) to ROS2. (See legacy branch)

- Navigation parameters need to be tuned

- Gazebo simulation: friction values etc need to be tuned.


## Troubleshooting:

### Substitutions in launch.xml
Some of the partial substitutions (Eg. $(sub)/abc/xyz.rviz) don't work well when used in `args`. An alternative is to define a separate variable and substitute that in `args` (Eg. A variable rviz_cfg_path is defined in tb3_empty_world.launch.xml and then this variable is used in `args` when launching rviz at the end of the launch file).

### On ros2-eloquent, in order to run Navigation2, BehaviorTree.CPP is required to be built from source (https://github.com/BehaviorTree/BehaviorTree.CPP/tree/ros2-devel)
https://github.com/ros-planning/navigation2/issues/1948

### LifeCyle nodes in Navigation2
All nodes in Navigation2 are LifeCycle nodes and thus need to be in the right state to function properly. You could use the Navigation2 tool (panel) in rviz to pause/reset these lifecycle nodes correctly.

### LaserScan not visible
In Rviz, the 'Reliability' setting for the LaserScan has to be changed to 'Best Effort' for rviz to visualize Laser Scans.