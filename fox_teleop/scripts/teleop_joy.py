#!/usr/bin/env python3

# Node to convert /joy messages to /cmd_vel
import rclpy
import threading
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

rclpy.init()
node = rclpy.create_node('teleop_joy')
rate = node.create_rate(30) # 30 Hz

node.declare_parameter('axis_linear', 1 )
node.declare_parameter('axis_angular', 0)
node.declare_parameter('scale_linear', 1)
node.declare_parameter('scale_angular', 1)

# Declare and get axes and scaling parameters
l_indx = node.get_parameter('axis_linear')
a_indx = node.get_parameter('axis_angular')
l_scale = node.get_parameter('scale_linear')
node.get_logger().info("Linear scaling: %s" % str(l_scale.value))
a_scale = node.get_parameter('scale_angular')
node.get_logger().info("Angular scaling: %s" % str(a_scale.value))

def joyCallback(joymsg):
    move.linear.x = l_scale*joymsg.axes[l_indx.value]
    move.angular.z = a_scale*joymsg.axes[a_indx.value]
    
# Subscribe to joy topic
node.create_subscription(Joy, 'joy', joyCallback, 1) # queue_size 1

# Publisher to cmd_vel
move = Twist()
pub_cmd_vel = node.create_publisher(Twist, 'cmd_vel', 1) # queue_size 1
# pub_cmd_vel = node.create_publisher(Twist, '/turtle1/cmd_vel', 1)


# Spin has to be done in a separate thread!
thread = threading.Thread(target=rclpy.spin, args=(node, ), daemon=True)
thread.start()

try:
    while rclpy.ok():
        pub_cmd_vel.publish(move)
        rate.sleep()
except KeyboardInterrupt:
    pass

# Destroy the node explicitly
# (optional - otherwise it will be done automatically
# when the garbage collector destroys the node object)
node.destroy_node()

rclpy.shutdown()
thread.join()