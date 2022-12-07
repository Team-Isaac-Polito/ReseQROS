#!/usr/bin/env python3

import rospy
from std_msgs.msg import UInt16
from ReseQROS.msg import Motor
from math import pi

def publisher():
    freq=100 # Hz
    Ts=1/freq

    pub_motor=rospy.Publisher("motor_topic",Motor,queue_size=10)
    motor_msg=Motor() #Motor.msg={wdx,wsx,angle}

    pub_flag=rospy.Publisher("flag",UInt16,queue_size=10)

    rate=rospy.Rate(freq)

    t=0
    T_tuning=5

    while not rospy.is_shutdown() and t<T_tuning:

        if t<1:
            motor_msg.wdx = 0
            motor_msg.wsx = 0
            motor_msg.angle = 0
            motor_msg.address = 21
        else:
            w_max=2*pi
            motor_msg.wdx = 1023
            motor_msg.wsx = 1023
            motor_msg.angle = 0
            motor_msg.address = 21

        t+=Ts

        pub_motor.publish(motor_msg)

        pub_flag.publish(0)

        rate.sleep()
    
    pub_flag.publish(1)
    motor_msg.wdx = 0
    motor_msg.wsx = 0
    motor_msg.angle = 0
    motor_msg.address = 21
    pub_motor.publish(motor_msg)


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