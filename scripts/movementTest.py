#!/usr/bin/env python3

import rospy
from ReseQROS.msg import Remote, Motor
from std_msgs.msg import UInt16, Float32


def assegnazione_velocità(vel,curv):
    vel = 512 if 462 <= vel <= 562 else vel # filtro
    vel = vel-512 # da 0/512/1023 a -512/0/511

    curv = 512 if 462 <= curv <= 562 else curv # filtro
    curv = curv-512 # da 0/512/1023 a -512/0/511

    #angolo
    angle = curv * 30 / 512 # da -512/0/512 a -30/0/30

    # definizione variabili strutturate per ROS
    pub=rospy.Publisher("motor_topic",Motor,queue_size=10)
    motor_msg=Motor() #Motor.msg={wdx,wsx,angle}

    motor_msg.wdx = (vel - curv/2) if vel >= 0 else vel
    motor_msg.wsx = (vel + curv/2) if vel >= 0 else vel
    motor_msg.angle = angle
    motor_msg.address = 21
    pub.publish(motor_msg) # ... tramette i valori wdx,wsx,angle sul topic "motor_topic"

    motor_msg.wdx = vel - curv / 4
    motor_msg.wsx = vel + curv / 4
    motor_msg.angle = angle
    motor_msg.address = 22
    pub.publish(motor_msg) # ... tramette i valori wdx,wsx,angle sul topic "motor_topic"
    
    motor_msg.wdx = (vel - curv/2) if vel < 0 else vel
    motor_msg.wsx = (vel + curv/2) if vel < 0 else vel
    motor_msg.address = 23
    pub.publish(motor_msg) # ... tramette i valori wdx,wsx,angle sul topic "motor_topic"

def vel_list(dataa):
    global vel
    vel=int(dataa.data)


def curv_list(dataa):
    global curv
    curv=int(dataa.data)
    assegnazione_velocità(vel,curv)


if __name__ == '__main__':
    try:
        rospy.init_node('agevar') #inizializza il nodo "agevar"
        rospy.loginfo("Hello! agevar node started!")

        rospy.Subscriber("vel",UInt16,vel_list)
        rospy.Subscriber("curv",UInt16,curv_list)

        rospy.spin()
        
    except rospy.ROSInterruptException:
        pass

