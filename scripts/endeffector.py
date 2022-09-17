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

def rescale(data):
    return (data-512)/512

def eex_list(dataa):
    eex_servo.value = rescale(dataa.data) 

def eey_list(dataa):
    #canbus
    out = dataa.data.to_bytes(2, byteorder='little', signed=True)
    # ToDo at the moment address is hardcoded
    msg = can.Message(arbitration_id=0x15,data=[definitions.DATA_PITCH, out[0], out[1]],is_extended_id=False) 
    canbus.send(msg)

def eez_list(dataa):
    eez_servo.value = rescale(dataa.data)



if __name__ == '__main__':
    try:
        rospy.init_node('endeffector') #inizializza il nodo "endeffector"
        rospy.loginfo("Hello! endeffector node started!")

        canbus = can.interface.Bus(channel='can0', bustype='socketcan')

        rospy.Subscriber("eex",UInt16,eex_list)
        rospy.Subscriber("eey",UInt16,eey_list)
        rospy.Subscriber("eez",UInt16,eez_list)
        
        rospy.spin()
        
    except rospy.ROSInterruptException:
        pass
