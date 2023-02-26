cmake_minimum_required(VERSION 3.5)
project(reseq_msgs)

set(CMAKE_CXX_STANDARD 14)

find_package(ament_cmake REQUIRED)
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

ament_export_dependencies(rosidl_default_runtime)

ament_package()
