#!/usr/bin/python

import rospy
from geometry_msgs.msg import PoseStamped
from gazebo_msgs.msg import ModelState

rospy.init_node('gazebo_model_update')

pos_gazebo = ModelState()
pos_gazebo.model_name = 'fox_cart'

# callback function on pose topic
def poseCallback(msg):
  # get global variables
  global pos_gazebo

  # fill gazebo position with the pose message
  pos_gazebo.pose = msg.pose

  # publish the gazebo position
  model_pub.publish(pos_gazebo)

# initialize subscriber and publisher
pose_sub = rospy.Subscriber('pose', PoseStamped, poseCallback)
model_pub = rospy.Publisher('gazebo/set_model_state', ModelState, queue_size = 1)

rate = rospy.Rate(20) # 20 Hz
while not rospy.is_shutdown():
  rate.sleep()
