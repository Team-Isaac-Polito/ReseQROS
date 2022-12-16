FROM dustynv/ros:noetic-ros-base-l4t-r35.1.0

RUN apt-get update && apt-get install -y build-essential python3-can \
    && rm -rf /var/likb/apt/lists/*

RUN mkdir -p /catkin_ws/src/
WORKDIR /catkin_ws
#RUN /bin/bash -c 'git clone https://github.com/Team-Isaac-Polito/ReseQROS.git src/ReseQROS'
COPY ./reseq-ros /catkin_ws/src/

RUN /bin/bash -c '. /opt/ros/noetic/setup.bash; catkin_make'
RUN /bin/bash -c '. /opt/ros/noetic/setup.bash; source devel/setup.bash'

COPY ./docker_utils/entrypoint.sh /ros_entrypoint.sh

#already done in FROM image ENTRYPOINT ["/ros_entrypoint.sh"]
#RUN echo 'source /opt/ros/${ROS_DISTRO}/setup.bash' >> /root/.bashrc

RUN echo 'source /catkin_ws/devel/setup.bash' >> /root/.bashrc

CMD /bin/bash -c '. /root/.bashrc; roslaunch ReseQROS ReseQ.launch'
CMD bash

WORKDIR /
