#!/usr/bin/env python3

import rospy
from agevar_constant import *

from std_msgs.msg import UInt16

def main_function():
    pub_lin_vel=rospy.Publisher("lin_vel",UInt16,queue_size=10)
    pub_r_curv=rospy.Publisher("r_curv",UInt16,queue_size=10)

    rospy.init_node('talker',anonymous=True)
    rate=rospy.Rate(500)

    t=0
    t_step=t_sim/4

    while not rospy.is_shutdown() and t<t_sim:

        if t<=t_step:
            print('dritto')
            lin_vel_msg=0 #512-int(512/t_step*t) # linear acceleration
            r_curv_msg=512
        elif t_step<t<=2*t_step:
            print('curva 1')
            lin_vel_msg=0
            r_curv_msg=1023
        elif 2*t_step<t<3*t_step:
            print('curva 2')
            lin_vel_msg=0
            r_curv_msg=0
        else:
            print('fermo')
            lin_vel_msg=512
            r_curv_msg=512

        t+=Ts

        pub_lin_vel.publish(lin_vel_msg)
        pub_r_curv.publish(r_curv_msg)

        rate.sleep()

if __name__ == '__main__':
	try:
		main_function()
	except rospy.ROSInterruptException:
		pass