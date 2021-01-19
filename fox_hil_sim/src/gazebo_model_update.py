#!/usr/bin/python

import rospy
# from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from gazebo_msgs.msg import ModelState

rospy.init_node('gazebo_model_update')

pose_gazebo = ModelState()
pose_gazebo.model_name = 'fox_cart'

# callback function on odom topic
def odomCallback(msg):
  # get global variables
  global pose_gazebo

  # fill gazebo position with the pose in the odom message
  pose_gazebo.pose = msg.pose.pose

  # publish the gazebo pose
  model_pub.publish(pose_gazebo)

# initialize subscriber and publisher
odom_sub = rospy.Subscriber('odom', Odometry, odomCallback)
# odom_sub = rospy.Subscriber('pose', PoseStamped, odomCallback)
model_pub = rospy.Publisher('gazebo/set_model_state', ModelState, queue_size = 1)

rate = rospy.Rate(20) # 20 Hz
while not rospy.is_shutdown():
  rate.sleep()
