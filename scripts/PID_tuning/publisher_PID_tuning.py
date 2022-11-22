#!/usr/bin/env python3

import rospy
from std_msgs.msg import UInt16

def publisher():
    freq=100 # Hz
    Ts=1/freq

    pub_lin_vel=rospy.Publisher("lin_vel",UInt16,queue_size=10)
    pub_r_curv=rospy.Publisher("r_curv",UInt16,queue_size=10)
    pub_flag=rospy.Publisher("flag",UInt16,queue_size=10)

    rate=rospy.Rate(freq)

    t=0
    T_tuning=5

    while not rospy.is_shutdown() and t<T_tuning:

        if t<1:
            lin_vel_msg=512
            r_curv_msg=512
        else:
            lin_vel_msg=0 # max velocity
            r_curv_msg=512

        t+=Ts

        pub_lin_vel.publish(lin_vel_msg)
        pub_r_curv.publish(r_curv_msg)

        rate.sleep()
    
    pub_flag.publish(1)

# Main function 
def main_function():
    rospy.init_node('publisher_PID_tuning')
    rospy.loginfo("Hello! publisher_PID_tuning node started!") 
    publisher()

if __name__ == '__main__':
	try:
		main_function()
	except rospy.ROSInterruptException:
		pass