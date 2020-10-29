cmake_minimum_required(VERSION 3.5)
project(fox_ekf)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)


# Commands to set up new message type
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)
set(msg_files
  "msg/Imu.msg"
)
rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
  DEPENDENCIES geometry_msgs std_msgs
)
ament_export_dependencies(rosidl_default_runtime)


# Add executable (the cpp file)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
add_executable(msgs_conversion
  src/msgs_conversion.cpp
)
ament_target_dependencies(msgs_conversion
  "rclcpp"
  "geometry_msgs"
  "sensor_msgs"
  "nav_msgs"  
)
install(TARGETS msgs_conversion
 DESTINATION lib/${PROJECT_NAME}
)

# Link againt interface (required for package from same interface!)
rosidl_target_interfaces(msgs_conversion
  ${PROJECT_NAME} "rosidl_typesupport_cpp")

# Install directories required
install(DIRECTORY
  launch
  msg
  params  
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
