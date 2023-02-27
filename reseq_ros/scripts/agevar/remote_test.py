#!/usr/bin/env python3

import rospy
from agevar_constant import *
from geometry_msgs.msg import Twist

def publisher():

    pub = rospy.Publisher("twist_joystick",Twist,queue_size=10)
    twist_msg = Twist()

    rate=rospy.Rate(freq)

    t=0
    t_in=2
    t_step=4
    t_sim=8

    while not rospy.is_shutdown() :                 

        if t<=t_in:
            print('fermo')
            lin_vel=0 # rest
            r_curv=0
        elif t_in<t<=t_step:
            print('dritto')
            lin_vel=500 # constant velocity
            r_curv=0
        elif t_step<t<=t_sim:
            print('curva')
            lin_vel=500
            r_curv=500    
        else:
            print('fermo')
            lin_vel=0 # rest
            r_curv=0
            break         

        twist_msg.linear.y = lin_vel
        twist_msg.linear.x = r_curv

        t+=Ts

        pub.publish(twist_msg)

        rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('remote_test')
        rospy.loginfo("Hello! remote_test node started!")

        rospy.sleep(2)

        publisher()
    except rospy.ROSInterruptException:
        pass