#!/usr/bin/env python3

import rospy
from agevar_constant import *
from geometry_msgs.msg import Twist

def publisher():

    pub = rospy.Publisher("twist_joystick",Twist,queue_size=10)
    twist_msg = Twist()

    rate=rospy.Rate(freq)

    t=0
    t_sim=1000
    t_step=1

    while not rospy.is_shutdown() :

        if t >= t_sim:
            print('fermo')
            lin_vel=512 # rest
            r_curv=512
            break      

        if t<=t_step:
            print('dritto')
            #lin_vel=512-int(512/t_step*2*t) # linear acceleration
            lin_vel=-512 # constant velocity
            r_curv=0
        elif t_step<t<t_sim:
            print('curva')
            lin_vel=-512
            r_curv=512            

        twist_msg.linear.y = lin_vel
        twist_msg.linear.x = r_curv

        t+=Ts

        pub.publish(twist_msg)

        rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('remote_test')
        rospy.loginfo("Hello! remote_test node started!")

        publisher()
    except rospy.ROSInterruptException:
        pass