#!/usr/bin/env python3

import rospy
from reseq_ros.msg import Motor

def publisher():
    pub=rospy.Publisher("motor_topic",Motor,queue_size=10)
    motor_msg=Motor() #Motor.msg={wdx,wsx,angle}

    rate = rospy.Rate(50)

    while not rospy.is_shutdown():

        omega = 1 #angular speed (max 1.15, the faster motor goes to 130 rpm)

        motor_msg.wdx = -10*omega*(cos(delta_max+2*b*sin(delta_max)/d))/(2*a*r_eq)  #10x is for scaling RIGHT????? (change everywere if is not)
        motor_msg.wsx = -10*omega*(cos(delta_max-2*b*sin(delta_max)/d))/(2*a*r_eq)
        motor_msg.angle = 0
        motor_msg.address = 21 # head

        pub.publish(motor_msg)

        motor_msg.wdx = 10*omega*2/(d*r_eq)
        motor_msg.wsx = -10*omega*2/(d*r_eq)
        motor_msg.angle = 0
        motor_msg.address = 22 # middle

        pub.publish(motor_msg)

        motor_msg.wdx = 10*omega*(cos(delta_max-2*b*sin(delta_max)/d))/(2*a*r_eq)
        motor_msg.wsx = 10*omega*(cos(delta_max+2*b*sin(delta_max)/d))/(2*a*r_eq)
        motor_msg.angle = 0
        motor_msg.address = 23 # tail

        pub.publish(motor_msg)

        rate.sleep()      

if __name__ == '__main__':
    try:
        rospy.init_node('turn_in_place')
        rospy.loginfo("Hello! turn_in_place node started!")

        publisher()

        #rospy.Subscriber("",,)

    except rospy.ROSInterruptException:
        pass
