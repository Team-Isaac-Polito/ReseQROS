#!/usr/bin/env python3

''' Andrea Grillo '''

import rospy
import can
import definitions
from std_msgs.msg import UInt16
from gpiozero import Servo
import time

PIN_EEX = 18
PIN_EEZ = 19

eex_servo = Servo(PIN_EEX)
eez_servo = Servo(PIN_EEZ)

eex_val = 0
eey_val = 1023
eez_val = 0

pitch_val = 0 # ToDo check starting Value

eex_time = eey_time = eez_time = pitch_time = time.time()


def rescale(data):
    data = 512 if 462 < data < 562 else data
    return (data-512)/(512*35)

def eex_list(dataa):
    global eex_val
    global eex_time

    act_time = time.time()
    eex_val += rescale(dataa.data) * (act_time - eex_time)
    eex_val = eex_val if -1 < eex_val < 1 else 1 if eex_val >= 1 else -1 
    eex_servo.value = eex_val
    eex_time = act_time

def eez_list(dataa):
    global eez_val
    global eez_time

    act_time = time.time()
    eez_val += rescale(dataa.data) * (act_time - eez_time)
    eez_val = eez_val if -1 < eez_val < 1 else 1 if eez_val >= 1 else -1 
    eez_servo.value = eez_val
    eez_time = act_time

def eey_list(dataa):
    global eey_val
    global eey_time

    act_time = time.time()
    dataa.data = 512 if 462 < dataa.data < 562 else dataa.data
    eey_val += ((dataa.data-512) / 35) * (act_time - eey_time)
    eey_val = eey_val if 0 < eey_val < 1023 else 1023 if eey_val >= 1023 else 0 

    # definizione variabili strutturate per ROS
    pub=rospy.Publisher("EE_topic",UInt16,queue_size=10)
    msg=UInt16() 
    msg.data = int(eey_val)
    pub.publish(msg)
    eey_time = act_time

def pitch_list(dataa):
    global pitch_val
    global pitch_time

    act_time = time.time()
    dataa.data = 512 if 462 < dataa.data < 562 else dataa.data
    pitch_val += ((dataa.data-512) / 35) * (act_time - eey_time)
    pitch_val = pitch_val if 0 < pitch_val < 1023 else 1023 if pitch_val >= 1023 else 0 

    # definizione variabili strutturate per ROS
    pub=rospy.Publisher("PITCH_can",UInt16,queue_size=10)
    msg=UInt16() 
    msg.data = int(pitch_val)
    pub.publish(msg)

    pitch_time = act_time



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
