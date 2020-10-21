# rofox packages

This repository contains the ROS packages for the RoFox robot by DoBots.
You may choose the branch as per your ROS distribution (The master branch assumes **ros1-melodic**).

Below you can find instructions on how to bringup the Gazebo simulation, run SLAM algorithms, localization or autonomous navigation.

## Source your workspace
```
source <workspace path>/devel/setup.bash
```

## Start the simulation with teleop

To launch the arena:
```
roslaunch fox_bringup fox_gazebo.launch
```
To start the keyboard teleop:

```
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```

To run RViz:
```
rosrun rviz rviz
```

## Start HectorSLAM
```
#1. Simulation
roslaunch fox_bringup fox_gazebo.launch

#2. Teleoperation
rosrun teleop_twist_keyboard teleop_twist_keyboard.py

#3. Hector SLAM
roslaunch fox_localization hector_mapping.launch

#4. RViz
rosrun rviz rviz
```

## Start GMapping
```
#1. Simulation
roslaunch fox_bringup fox_gazebo.launch

#2. Teleoperation
rosrun teleop_twist_keyboard teleop_twist_keyboard.py

#3. GMapping
roslaunch fox_localization gmapping.launch

#4. RViz
rosrun rviz rviz
```

## Start AMCL
```
#1. Simulation
roslaunch fox_bringup fox_gazebo.launch

#2. Teleoperation
rosrun teleop_twist_keyboard teleop_twist_keyboard.py

#3. Map server
roslaunch fox_localization map.launch

#4. AMCL
roslaunch fox_localization amcl.launch

#5. RViz
rosrun rviz rviz
```

## Start autonomous navigation (move_base) with GMapping 
```
#1. Simulation
roslaunch fox_bringup fox_gazebo.launch

#2. Teleoperation
rosrun teleop_twist_keyboard teleop_twist_keyboard.py

#3. GMapping
roslaunch fox_localization gmapping.launch

#4. RViz
rosrun rviz rviz

#5. Move_base
roslaunch fox_navigation move_base.launch 
```

## Start autonomous navigation(move_base) with AMCL 
```
#1. Simulation
roslaunch fox_bringup fox_gazebo.launch

#2. Teleoperation
rosrun teleop_twist_keyboard teleop_twist_keyboard.py

#3. Map server
roslaunch fox_localization map.launch

#4. AMCL
roslaunch fox_localization amcl.launch

#5. RViz
rosrun rviz rviz

#6. Move_base
roslaunch fox_navigation move_base.launch 
```

### ToDo:

- Navigation parameters need to be tuned

- Gazebo simulation: friction values etc need to be tuned.