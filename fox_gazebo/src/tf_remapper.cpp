#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "tf2_msgs/msg/tf_message.hpp"
#include <geometry_msgs/msg/transform_stamped.h>
using std::placeholders::_1;

/* This node remaps tfs from a namespaced tf topic to the /tf topic. */
/* Example usage: 
ros2 run fox_gazebo tf_remapper --ros-args -p "from_topic:=/robot_0/tf" */

class TF_Remapper : public rclcpp::Node
{
  public:
    TF_Remapper()
    : Node("tf_remapper")
    {
      // Get 'from' and 'to' strings using param
      this->declare_parameter<std::string>("from_topic", "tf");
      this->get_parameter("from_topic", from_topic_string_);
      
      this->declare_parameter<std::string>("to_topic", "/tf");
      this->get_parameter("to_topic", to_topic_string_);      
      
      // Get tf_prefix from param
      this->declare_parameter<std::string>("tf_prefix", "");
      this->get_parameter("tf_prefix", tf_prefix_string_);

      // Create two subscribers to specified tf and tf_static topics
      tf_subscription_ = this->create_subscription<tf2_msgs::msg::TFMessage>(
      from_topic_string_, 100, std::bind(&TF_Remapper::tf_callback, this, _1));
      tf_static_subscription_ = this->create_subscription<tf2_msgs::msg::TFMessage>(
      from_topic_string_+"_static", 100, std::bind(&TF_Remapper::tf_static_callback, this, _1));

      // Create two publishers to specified tf and tf_static topics
      tf_publisher_ = this->create_publisher<tf2_msgs::msg::TFMessage>(to_topic_string_, 100);
      tf_static_publisher_ = this->create_publisher<tf2_msgs::msg::TFMessage>(to_topic_string_+"_static", 100);

      RCLCPP_INFO(this->get_logger(), "Subscribing to: '%s' (and _static)", tf_subscription_->get_topic_name());
      RCLCPP_INFO(this->get_logger(), "Publishing to: '%s' (and _static)", tf_publisher_->get_topic_name());
    }

  private:
    void tf_callback(const tf2_msgs::msg::TFMessage::SharedPtr msg)
    {
      tf2_msgs::msg::TFMessage output_msg;

      for (const auto & transform : msg->transforms) {
        // Append prefix to frame names
        geometry_msgs::msg::TransformStamped output_tf = transform;
        output_tf.header.frame_id = tf_prefix_string_ + transform.header.frame_id;
        output_tf.child_frame_id = tf_prefix_string_ + transform.child_frame_id;

        output_msg.transforms.push_back(output_tf);
      }
      
      tf_publisher_->publish(output_msg);
    }
    
    void tf_static_callback(const tf2_msgs::msg::TFMessage::SharedPtr msg)
    {
      tf2_msgs::msg::TFMessage output_msg;

      for (const auto & transform : msg->transforms) {
        // Append prefix to frame names
        geometry_msgs::msg::TransformStamped output_tf = transform;
        output_tf.header.frame_id = tf_prefix_string_ + transform.header.frame_id;
        output_tf.child_frame_id = tf_prefix_string_ + transform.child_frame_id;

        output_msg.transforms.push_back(output_tf);
      }
      
      tf_static_publisher_->publish(output_msg);
    }

    std::string from_topic_string_;
    std::string to_topic_string_;
    std::string tf_prefix_string_;
    rclcpp::Subscription<tf2_msgs::msg::TFMessage>::SharedPtr tf_subscription_;
    rclcpp::Subscription<tf2_msgs::msg::TFMessage>::SharedPtr tf_static_subscription_;
    rclcpp::Publisher<tf2_msgs::msg::TFMessage>::SharedPtr tf_publisher_;
    rclcpp::Publisher<tf2_msgs::msg::TFMessage>::SharedPtr tf_static_publisher_;
  };

  int main(int argc, char * argv[])
  {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<TF_Remapper>());
    rclcpp::shutdown();
    return 0;
  }