#!/usr/bin/env python3

import rospy
from reseq_ros.msg import Motor
from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist

def list(data):
    v = data.linear.y
    w = data.linear.x

    vel =  ((512 - abs(w)) * (v / 512) + v)
    curv = -((512 - abs(v)) * (w / 512) + w)

    #angolo
    angle = curv * 30 / 512 # da -512/0/512 a -30/0/30

    # definizione variabili strutturate per ROS
    pub=rospy.Publisher("motor_topic",Motor,queue_size=10)
    motor_msg=Motor() #Motor.msg={wdx,wsx,angle}

    motor_msg.wdx = int((vel - curv) if vel <= 0 else (vel + curv/4))
    motor_msg.wsx = int((vel + curv) if vel <= 0 else (vel - curv/4))
    motor_msg.angle = angle
    motor_msg.address = 21
    print("IND "+ str(motor_msg.address) + " dx " + str(motor_msg.wdx) + " sx " + str(motor_msg.wsx))
    pub.publish(motor_msg) # ... tramette i valori wdx,wsx,angle sul topic "motor_topic"

    motor_msg.wdx = int((vel - curv/2) if vel <= 0 else (vel + curv/4))
    motor_msg.wsx = int((vel + curv/2) if vel <= 0 else (vel - curv/4))
    motor_msg.angle = angle
    motor_msg.address = 22
    print("IND "+ str(motor_msg.address) + " dx " + str(motor_msg.wdx) + " sx " + str(motor_msg.wsx))
    pub.publish(motor_msg) # ... tramette i valori wdx,wsx,angle sul topic "motor_topic"

    motor_msg.wdx = int((vel - curv/4) if vel <= 0 else (vel + curv))
    motor_msg.wsx = int((vel + curv/4) if vel <= 0 else (vel - curv))
    motor_msg.address = 23
    print("IND "+ str(motor_msg.address) + " dx " + str(motor_msg.wdx) + " sx " + str(motor_msg.wsx))
    pub.publish(motor_msg) # ... tramette i valori wdx,wsx,angle sul topic "motor_topic"

if __name__ == '__main__':
    try:
        rospy.init_node('agevar') #inizializza il nodo "agevar"
        rospy.loginfo("Hello! agevar node started!")

        rospy.Subscriber("twist_joystick",Twist,list)

        rospy.spin()
    except rospy.ROSInterruptException:
        pass

