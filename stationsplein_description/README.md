﻿export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/projects/src/stationsplein_description/models/


## Simple shapes and a mesh file environment description

ROS package, which includes the mesh files, sdf description, world description and a launch file to launch  a world with a mesh file of the Stationsplein in Rotterdam.

To launch the world file include the following in your launch file:

    <include file="$(find gazebo_ros)/launch/empty_world.launch">
    <arg name="world_name" value="$(find stationsplein_description)/worlds/stationsplein_world.world"/>
    </include>

## Edit the package.xml file

It is desirable to make the codes easily portable and therefore all the mesh files should be stored in this package instead of the .gazebo/models folder. This can be achieved by editing the package.xml file in the current package to add it to the gazebo model path:

    <export>
        <!-- Other tools can request additional information be placed here -->
        <!-- gazebo_ros_paths_plugin automatically adds these to
        GAZEBO_PLUGIN_PATH and GAZEBO_MODEL_PATH when you do this export inside
        the package.xml file. -->
        <gazebo_ros gazebo_plugin_path="${prefix}/lib"/>
        <gazebo_ros gazebo_model_path="${prefix}/models"/>
        <gazebo_ros gazebo_media_path="${prefix}/models"/>
    </export>


