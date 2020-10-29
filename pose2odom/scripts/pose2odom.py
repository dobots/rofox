#!/usr/bin/env python3

# import
import rclpy
import threading
from rclpy.node import Node
from rclpy.qos import QoSProfile
import tf2_ros
from geometry_msgs.msg import Point, Pose, PoseStamped, Quaternion, TransformStamped
from nav_msgs.msg import Odometry

rclpy.init()
node = rclpy.create_node('publish_odom_node')

odom_pub = node.create_publisher(Odometry, 'odom', 1) # queue_size 1

# Broadcaster to send the tranform (publish transform)
qos_profile = QoSProfile(depth=10) # QOS profile (Optional)
br = tf2_ros.TransformBroadcaster(node, qos=qos_profile) # Broadcaster

# callback function of topic pose data
# this function reads the incoming message and converts it to an odom message, which it publishes
def callback(msg):
	global odom_pub

	# Fill transform message with incoming data
	odom_trans = TransformStamped()
	current_time = node.get_clock().now()
	odom_trans.header.stamp = current_time.to_msg()
	odom_trans.header.frame_id = "odom"
	odom_trans.child_frame_id = "base_link"
	odom_trans.transform.translation.x = msg.pose.position.x
	odom_trans.transform.translation.y = msg.pose.position.y
	odom_trans.transform.translation.z = 0.
	odom_trans.transform.rotation = Quaternion(x=msg.pose.orientation.x, y=msg.pose.orientation.y, z=msg.pose.orientation.z, w=msg.pose.orientation.w)

	# Broadcast to send the tranform (publish transform)
	br.sendTransform(odom_trans)

	# Fill odom message with incoming data
	odom_msg = Odometry()
	odom_msg.header.stamp = current_time.to_msg()
	odom_msg.header.frame_id = "odom"
	odom_msg.child_frame_id = "base_link"
	odom_msg.pose.pose = Pose(position=Point(x=msg.pose.position.x,y=msg.pose.position.y,z=msg.pose.position.z), orientation=Quaternion(x=msg.pose.orientation.x, y=msg.pose.orientation.y, z=msg.pose.orientation.z, w=msg.pose.orientation.w))

	# Publish odom message
	odom_pub.publish(odom_msg)

# Create subscriber
node.create_subscription(PoseStamped, 'pose', callback, 1) # queue_size 1
	
# Spin has to be done in a separate thread!
thread = threading.Thread(target=rclpy.spin, args=(node, ), daemon=True)
thread.start()

try:
    while rclpy.ok():
        pass
except KeyboardInterrupt:
    pass

# Destroy the node explicitly
# (optional - otherwise it will be done automatically
# when the garbage collector destroys the node object)
node.destroy_node()

rclpy.shutdown()
thread.join()

