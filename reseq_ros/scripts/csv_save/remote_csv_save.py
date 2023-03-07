#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import csv

flag = 0
v = []
r = []

def callback(dataa):
    global flag, v, r

    lin_vel = dataa.linear.y
    r_curv = dataa.linear.x

    if abs(lin_vel)>50:
        flag = 1
        v.append(lin_vel)
        r.append(r_curv)
    elif abs(lin_vel)<50 and flag == 1:
        flag = 2
        csv_func()

def csv_func():
    global flag, v, r
    with open('remote.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(v)
        writer.writerow(r)

if __name__ == '__main__':
    try:
        rospy.init_node('csv_save_node')
        rospy.loginfo("Hello! csv_save_node node started!")

        sub = rospy.Subscriber('twist_joystick',Twist,callback)
            
        rospy.spin()

    except rospy.ROSInterruptException:
        pass