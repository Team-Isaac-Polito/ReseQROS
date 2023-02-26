FROM dustynv/ros:humble-ros-base-l4t-r35.1.0

RUN apt-get update && apt-get install -y python3-pip build-essential python3-can \
    && rm -rf /var/likb/apt/lists/*
RUN pip3 install matplotlib

RUN mkdir -p /ros2_ws/src/
WORKDIR /ros2_ws

COPY reseq_ros/CMakeLists.txt src/
COPY reseq_ros/package.xml src/
COPY reseq_ros/msg src/msg

RUN /bin/bash -c '. /opt/ros/$ROS_DISTRO/setup.bash; colcon build'

COPY ./docker_utils/entrypoint.sh /ros_entrypoint.sh

COPY reseq_ros/launch src/launch
COPY reseq_ros/scripts src/scripts

CMD roslaunch reseq_ros ReseQ.launch
