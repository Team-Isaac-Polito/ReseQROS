FROM dustynv/ros:humble-ros-base-l4t-r35.1.0

RUN apt-get update && apt-get install -y python3-pip build-essential python3-can \
    && rm -rf /var/likb/apt/lists/*
RUN pip3 install matplotlib

RUN mkdir -p /ros2_ws/src/
WORKDIR /ros2_ws

COPY reseq_msgs src/reseq_msgs
COPY reseq_ros src/reseq_ros

RUN /bin/bash -c '. /opt/ros/$ROS_DISTRO/install/setup.bash; colcon build'

COPY ./docker_utils/entrypoint.sh /ros_entrypoint.sh

CMD roslaunch reseq_ros ReseQ.launch
