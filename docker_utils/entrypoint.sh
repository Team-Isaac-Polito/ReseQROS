#!/bin/bash
set -e

ros_env_setup="/opt/ros/$ROS_DISTRO/install/setup.bash"
echo "sourcing   $ros_env_setup"
source "$ros_env_setup"
ros_env_setup="/ros2_ws/install/setup.bash"
echo "sourcing   $ros_env_setup"
source "$ros_env_setup"


export ROS_IP=10.142.10.9
export ROS_HOSTNAME=10.142.10.9
export ROS_MASTER_URI=http://10.142.10.9:11311

echo "ROS_ROOT   $ROS_ROOT"
echo "ROS_DISTRO $ROS_DISTRO"

exec "$@"
