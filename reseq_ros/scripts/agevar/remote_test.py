#!/usr/bin/env python3

import rospy
from agevar_constant import *
from geometry_msgs.msg import Twist

def publisher():

    pub = rospy.Publisher("twist_joystick",Twist,queue_size=10)
    twist_msg = Twist()

    rate=rospy.Rate(freq)

    t=0
    t_sim=5
    t_step=t_sim/4

    while not rospy.is_shutdown() and t<t_sim:

        if t<=t_step:
            print('dritto')
            lin_vel=0 #512-int(512/t_step*t) # linear acceleration
            r_curv=512
        elif t_step<t<=2*t_step:
            print('curva 1')
            lin_vel=0
            r_curv=1023
        elif 2*t_step<t<3*t_step:
            print('curva 2')
            lin_vel=0
            r_curv=0
        else:
            print('fermo')
            lin_vel=512
            r_curv=512

        twist_msg.linear.y = lin_vel
        twist_msg.linear.x = r_curv

        t+=Ts

        pub.publish(twist_msg)

        rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('remote_test')
        rospy.loginfo("Hello! agevar_in node started!")

        publisher()
    except rospy.ROSInterruptException:
        pass