#include "rclcpp/rclcpp.hpp"
#include "fox_ekf/msg/imu.hpp"
#include "geometry_msgs/msg/pose_stamped.hpp"
#include "sensor_msgs/msg/imu.hpp"
#include "nav_msgs/msg/odometry.hpp"

#define ODOM_COV 0.005
#define ODOM_ORIENTATION_COV 0.1
#define IMU_ORIENTATION_COV 0.05
#define IMU_ORIENTATION_Z_COV 0.005
#define IMU_ANG_VEL_COV 0.1
#define IMU_LIN_ACCEL_COV 0.5
#define PI 3.1415
#define G_ACCEL 9.8066

nav_msgs::msg::Odometry odom_msg;
sensor_msgs::msg::Imu imu_msg;

bool odom_pub_flag = false;
bool imu_pub_flag = false;

// rclcpp::Publisher<fox_ekf::msg::Imu>::SharedPtr odom_pub_ptr;
// rclcpp::Publisher<geometry_msgs::msg::PoseStamped>::SharedPtr imu_pub_ptr;

void poseCallback(const geometry_msgs::msg::PoseStamped::SharedPtr pose_msg)
{

  odom_msg.pose.pose.orientation.x = pose_msg->pose.orientation.x;
  odom_msg.pose.pose.orientation.y = pose_msg->pose.orientation.y;
  odom_msg.pose.pose.orientation.z = pose_msg->pose.orientation.z;
  odom_msg.pose.pose.orientation.w = pose_msg->pose.orientation.w;

  odom_msg.pose.pose.position.x = pose_msg->pose.position.x;
  odom_msg.pose.pose.position.y = pose_msg->pose.position.y;
  odom_msg.pose.pose.position.z = pose_msg->pose.position.z;

  odom_msg.pose.covariance[0] = ODOM_COV;
  odom_msg.pose.covariance[7] = ODOM_COV;
  odom_msg.pose.covariance[14] = ODOM_COV;
  odom_msg.pose.covariance[21] = ODOM_ORIENTATION_COV;
  odom_msg.pose.covariance[28] = ODOM_ORIENTATION_COV;
  odom_msg.pose.covariance[35] = ODOM_ORIENTATION_COV;

  odom_msg.header = pose_msg->header;

  odom_pub_flag = true;

}

void mpuCallback(const fox_ekf::msg::Imu::SharedPtr mpu_msg)
{

  imu_msg.header = mpu_msg->header;
  imu_msg.header.frame_id = "imu_link";

  imu_msg.orientation.x = mpu_msg->orientation.x;
  imu_msg.orientation.y = mpu_msg->orientation.y;
  imu_msg.orientation.z = mpu_msg->orientation.z;
  imu_msg.orientation.w = mpu_msg->orientation.w;

  imu_msg.angular_velocity.x = mpu_msg->angular_velocity[0] * PI / 180;
  imu_msg.angular_velocity.y = mpu_msg->angular_velocity[1] * PI / 180;
  imu_msg.angular_velocity.z = mpu_msg->angular_velocity[2] * PI / 180;

  imu_msg.linear_acceleration.x = mpu_msg->linear_acceleration[0] * G_ACCEL;
  imu_msg.linear_acceleration.y = mpu_msg->linear_acceleration[1] * G_ACCEL; 
  imu_msg.linear_acceleration.z = mpu_msg->linear_acceleration[2] * G_ACCEL; 

  imu_msg.orientation_covariance[0] = IMU_ORIENTATION_COV;
  imu_msg.orientation_covariance[4] = IMU_ORIENTATION_COV;
  imu_msg.orientation_covariance[8] = IMU_ORIENTATION_COV;
  imu_msg.orientation_covariance[8] = IMU_ORIENTATION_Z_COV;

  imu_msg.angular_velocity_covariance[0] = IMU_ANG_VEL_COV;
  imu_msg.angular_velocity_covariance[4] = IMU_ANG_VEL_COV;
  imu_msg.angular_velocity_covariance[8] = IMU_ANG_VEL_COV;

  imu_msg.linear_acceleration_covariance[0] = IMU_LIN_ACCEL_COV;
  imu_msg.linear_acceleration_covariance[4] = IMU_LIN_ACCEL_COV;
  imu_msg.linear_acceleration_covariance[8] = IMU_LIN_ACCEL_COV;

  imu_pub_flag = true;

}


int main(int argc, char **argv)
{

  rclcpp::init(argc, argv);
  auto node = rclcpp::Node::make_shared("msgs_conversion");

  auto imu_pub = node->create_publisher<sensor_msgs::msg::Imu>("/imu", 1);
  // imu_pub_ptr = imu_pub;

  auto odom_pub = node->create_publisher<nav_msgs::msg::Odometry>("/odom/wheel", 1);  
  // odom_pub_ptr = odom_pub;

  auto mpu_sub = node->create_subscription<fox_ekf::msg::Imu>("/mpu9250", 1000, mpuCallback);
  auto pose_sub = node->create_subscription<geometry_msgs::msg::PoseStamped>("/pose", 1000, poseCallback);

  rclcpp::Rate loop_rate(20);

  while (rclcpp::ok())
  {
    rclcpp::spin_some(node);
    
    odom_pub->publish(odom_msg);
    odom_pub_flag = false;
    imu_pub->publish(imu_msg);
    imu_pub_flag = false;
    
    loop_rate.sleep();
  }

  return 0;
}
