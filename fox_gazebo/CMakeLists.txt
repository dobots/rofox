cmake_minimum_required(VERSION 3.5)
project(fox_gazebo)

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
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

add_executable(tf_remapper src/tf_remapper.cpp)
ament_target_dependencies(tf_remapper rclcpp std_msgs tf2_ros tf2_msgs geometry_msgs)

# Install executable files
install(TARGETS
  tf_remapper
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY
  launch
  worlds
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
