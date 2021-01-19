# Copyright (c) 2020 Open Source Robotics Foundation, Inc.
# All rights reserved.
#
# Software License Agreement (BSD License 2.0)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# This launch file shows how to launch robot_state_publisher with a URDF
# first processed using the xacro python API.

import os

import launch
import launch_ros.actions
from launch_ros.substitutions import FindPackageShare

import xacro
import xml.etree.ElementTree as ET

def generate_launch_description():
    # Simulation (Gazebo) time
    use_sim_time = launch.substitutions.LaunchConfiguration('use_sim_time', default='false')

    # Urdf using xacro command substitution
    pkg_share = FindPackageShare('fox_description').find('fox_description')
    urdf_dir = os.path.join(pkg_share, 'urdf')
    urdf_path = os.path.join(urdf_dir, 'base_fox_cart.urdf')
    # If urdf isn't already built, build it here using xacro
    xacro_path = urdf_path + '.xacro'
    doc = xacro.process_file(xacro_path)
    robot_desc = doc.toprettyxml(indent='  ')

    # Optional: remap tfs of gazebo plugins
    # TODO: Find best way to pass arguement to python launch file from xml launch file.
    # tf_remapping = launch.substitutions.LaunchConfiguration('tf_remapping', default='/tf:=tf')
    # f = open(urdf_path, "w")
    # f.write(robot_desc)
    # f.close()
    # xml_tree = ET.parse(urdf_path)
    # xml_root = xml_tree.getroot()
    # for plugin in xml_root.iter('plugin'):
    #     if 'base_fox_controller' in plugin.attrib.values():
    #         # The only plugin we care for now is 'diff_drive' which is
    #         # broadcasting a transform between`odom` and `base_footprint`
    #         break
    # xml_tf_remap = ET.SubElement(plugin.find('ros'), 'remapping')
    # xml_tf_remap.text = tf_remapping
    # robot_desc = ET.tostring(xml_root, encoding='unicode')
  
    # Launch robot_state_publisher with urdf as robot description param
    params = {'robot_description': robot_desc,
              'publish_frequency': 30.0,
              'use_sim_time': use_sim_time,
              'use_tf_static': False}

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
                                'use_sim_time',
                                default_value='false',
                                description='Use simulation (Gazebo) clock if true'),
        launch_ros.actions.Node(package='robot_state_publisher',
                                executable='robot_state_publisher',
                                remappings=[("/tf", "tf"), ('/tf_static', 'tf_static')], # Tf relative namespace for remapping
                                output='screen',                                
                                parameters=[params])
    ])