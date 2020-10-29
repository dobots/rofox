#!/usr/bin/env python

# import
import rospy
from geometry_msgs.msg import Point, Pose, PoseStamped, Quaternion, TransformStamped
from nav_msgs.msg import Odometry
import tf

odom_pub = rospy.Publisher("odom", Odometry, queue_size=1)

# callback function of topic pose data
# this function reads the incoming message and converts it to an odom message, which it publishes
def callback(msg):
	global odom_pub

	# Fill transform message with incoming data
	odom_trans = TransformStamped()
	current_time = rospy.Time.now()

	# Fill odom msg with pose msg
	x = msg.pose.position.x
	y = msg.pose.position.y
	z = 0
	quat_x = msg.pose.orientation.x
	quat_y = msg.pose.orientation.y
	quat_z = msg.pose.orientation.z
	quat_w = msg.pose.orientation.w

	# Broadcast to send the tranform (publish transform)
	odom_broadcaster = tf.TransformBroadcaster()
	odom_broadcaster.sendTransform(
		(x,y,z),
		(quat_x, quat_y, quat_z, quat_w),
		current_time,
		"base_link",
		"odom"
	)

	# Fill odom message with incoming data
	odom_msg = Odometry()
	odom_msg.header.stamp = current_time
	odom_msg.header.frame_id = "odom"
	odom_msg.child_frame_id = "base_link"
	odom_msg.pose.pose = Pose(Point(x,y,z), Quaternion(quat_x, quat_y, quat_z, quat_w))

	# Publish odom message
	odom_pub.publish(odom_msg)


# Class listener initializes a subscriber on the topic pose
def listener():
	rospy.Subscriber("pose", PoseStamped, callback)

if __name__ == '__main__':
	rospy.init_node("publish_odom_node", anonymous=True)
	listener()
	rospy.spin()


