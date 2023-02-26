cmake_minimum_required(VERSION 3.5)
project(reseq_ros)

set(CMAKE_CXX_STANDARD 14)

find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

## Generate messages in the 'msg' folder
set(msg_files
   "msg/Motor.msg"
   "msg/RealInput.msg"
   "msg/RealMotor.msg"
   "msg/RealOutput.msg"
)

rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
)

catkin_package(
  CATKIN_DEPENDS message_runtime
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
