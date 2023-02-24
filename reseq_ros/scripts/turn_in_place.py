#!/usr/bin/env python3

import rospy
from reseq_ros.msg import Motor

def publisher():
    pub=rospy.Publisher("motor_topic",Motor,queue_size=10)
    motor_msg=Motor() #Motor.msg={wdx,wsx,angle}

    rate = rospy.Rate(50)

    while not rospy.is_shutdown():

        vel = 500

        motor_msg.wdx = -vel
        motor_msg.wsx = -vel
        motor_msg.angle = 0
        motor_msg.address = 21 # head

        pub.publish(motor_msg)

        motor_msg.wdx = vel
        motor_msg.wsx = -vel
        motor_msg.angle = 0
        motor_msg.address = 22 # middle

        pub.publish(motor_msg)

        motor_msg.wdx = vel
        motor_msg.wsx = vel
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