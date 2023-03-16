#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import Header
import matplotlib.pyplot as plt

i=0

# Callback function
def callback(dataa):
    global i
    if i == 0:
        header = dataa.header
        seq = header.seq
        stamp = header.stamp
        frame_id = header.frame_id
        height = dataa.height
        width = dataa.width
        fields =  dataa.fields
        dataa.is_bigendian
        dataa.point_step
        dataa.row_step
        dataa.data
        dataa.is_dense

        print(len(dataa.data))
        print(dataa.is_dense)
        # plt.imshow(list(dataa.data))
        # plt.show()
        i = i+1
    # print(msg.decode(encoding='utf-8',errors='strict'))
    return


if __name__ == '__main__':
    try:
        rospy.init_node('data_acquisition')
        rospy.loginfo("Hello! data_acquisition node started!") 
        
        rospy.Subscriber("/camera/depth/color/points",PointCloud2,callback)

        rospy.spin()
    except rospy.ROSInterruptException:
        pass