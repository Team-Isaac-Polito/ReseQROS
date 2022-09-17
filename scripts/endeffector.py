#!/usr/bin/env python3

''' Andrea Grillo ''''

import rospy
from std_msgs.msg import UInt16
from gpiozero import Servo

PIN_EEX = 18
PIN_EEZ = 19

eex_servo = Servo(PIN_EEX)
eez_servo = Servo(PIN_EEZ)

def rescale(data):
    return (data-512)/512

def eex(dataa):
    eex_servo.value = rescale(dataa.data) 

def eey(dataa):
    #canbus
    print("todo canbus")

def eez(dataa):
    eez_servo.value = rescale(dataa.data)



if __name__ == '__main__':
    try:
        rospy.init_node('endeffector') #inizializza il nodo "endeffector"
        rospy.loginfo("Hello! endeffector node started!")

        rospy.Subscriber("eex",UInt16,eex_list)
        rospy.Subscriber("eey",UInt16,eey_list)
        rospy.Subscriber("eez",UInt16,eez_list)
        
        rospy.spin()
        
    except rospy.ROSInterruptException:
        pass