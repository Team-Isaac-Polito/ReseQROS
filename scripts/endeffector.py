#!/usr/bin/env python3

''' Andrea Grillo '''

import rospy
import can
import definitions
from std_msgs.msg import UInt16
from gpiozero import Servo

PIN_EEX = 18
PIN_EEZ = 19

eex_servo = Servo(PIN_EEX)
eez_servo = Servo(PIN_EEZ)

eex_val = 0
eey_val = 1023
eez_val = 0

pitch_val = 0 # ToDo check starting Value

def rescale(data):
    data = 512 if 462 < data < 562 else data
    return (data-512)/(512*35)

def eex_list(dataa):
    global eex_val
    eex_val += rescale(dataa.data)
    eex_val = eex_val if -1 < eex_val < 1 else 1 if eex_val >= 1 else -1 
    eex_servo.value = eex_val

def eez_list(dataa):
    global eez_val
    eez_val += rescale(dataa.data)
    eez_val = eez_val if -1 < eez_val < 1 else 1 if eez_val >= 1 else -1 
    eez_servo.value = eez_val

def eey_list(dataa):
    #canbus
    dataa.data = 512 if 462 < dataa.data < 562 else dataa.data
    global eey_val
    eey_val += (dataa.data-512) / 35
    eey_val = eey_val if 0 < eey_val < 1023 else 1023 if eey_val >= 1023 else 0 

    # definizione variabili strutturate per ROS
    pub=rospy.Publisher("EE_topic",UInt16,queue_size=10)
    msg=UInt16() 
    msg.data = int(eey_val)
    pub.publish(msg)

def pitch_list(dataa):
    #canbus
    dataa.data = 512 if 462 < dataa.data < 562 else dataa.data
    global pitch_val
    pitch_val += (dataa.data-512) / 35
    pitch_val = pitch_val if 0 < pitch_val < 1023 else 1023 if pitch_val >= 1023 else 0 

    # definizione variabili strutturate per ROS
    pub=rospy.Publisher("PITCH_can",UInt16,queue_size=10)
    msg=UInt16() 
    msg.data = int(pitch_val)
    pub.publish(msg)



if __name__ == '__main__':
    try:
        rospy.init_node('endeffector') #inizializza il nodo "endeffector"
        rospy.loginfo("Hello! endeffector node started!")

        canbus = can.interface.Bus(channel='can0', bustype='socketcan')

        rospy.Subscriber("eex",UInt16,eex_list)
        rospy.Subscriber("eey",UInt16,eey_list)
        rospy.Subscriber("eez",UInt16,eez_list)

        rospy.Subscriber("pitch",UInt16,pitch_list)

        rospy.spin()
        
    except rospy.ROSInterruptException:
        pass
