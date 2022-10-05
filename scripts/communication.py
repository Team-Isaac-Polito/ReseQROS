#!/usr/bin/python3

import definitions
import can
import os
import time
import rospy
from ReseQROS.msg import Motor
from std_msgs.msg import UInt16


eex_val = 512
eey_val = 1023
eez_val = 512
pitch_val = 0 # ToDo check starting Value

eex_time = eey_time = eez_time = pitch_time = time.time()


def filter_center(data):
    return 512 if 462 < data < 562 else data
def interval(data):
    return data if 0 <= data <= 1023 else 1023 if data > 1023 else 0 


def motor_list(dataa):
    out = int(dataa.wsx).to_bytes(2, byteorder='little', signed=True)
    msg = can.Message(arbitration_id=int(dataa.address),data=[definitions.DATA_TRACTION_LEFT, out[0], out[1]],is_extended_id=False)
    canbus.send(msg)

    out = int(dataa.wdx).to_bytes(2, byteorder='little', signed=True)
    msg = can.Message(arbitration_id=int(dataa.address),data=[definitions.DATA_TRACTION_RIGHT, out[0], out[1]],is_extended_id=False)
    canbus.send(msg)

    out = int(dataa.angle).to_bytes(2, byteorder='little', signed=True)
    msg = can.Message(arbitration_id=int(dataa.address),data=[definitions.DATA_YAW, out[0], out[1]],is_extended_id=False)
    canbus.send(msg)


def pitch_list(dataa):
    global pitch_val
    global pitch_time

    act_time = time.time()
    dataa.data = filter_center(dataa.data)
    pitch_val += ((dataa.data-512) / 6000) * (act_time - eey_time)
    pitch_val = interval(pitch_val)
    out = int(pitch_val).to_bytes(2, byteorder='little', signed=True)
    pitch_time = act_time
    # ToDo at the moment address is hardcoded
    msg = can.Message(arbitration_id=0x17,data=[definitions.DATA_PITCH, out[0], out[1]],is_extended_id=False) 
    canbus.send(msg)


def ee_pitch_list(dataa):
    global eey_val
    global eey_time
    global eez_val
    global eez_time

    act_time = time.time()
    dataa.data = filter_center(dataa.data)
    eey_val += (dataa.data-512) * (act_time - eey_time)
    eey_val = interval(eey_val)
    eey_time = act_time

    out = int(eey_val).to_bytes(2, byteorder='little', signed=True)
    # ToDo at the moment address is hardcoded
    msg = can.Message(arbitration_id=0x15,data=[definitions.DATA_EE_PITCH, out[0], out[1]],is_extended_id=False) 
    canbus.send(msg)

    act_time = time.time()
    eez_val += (filter_center(dataa.data)-512) * (act_time - eez_time)
    eez_val = interval(eez_val)
    eez_time = act_time

    out = int(eez_val).to_bytes(2, byteorder='little', signed=True)
    # ToDo at the moment address is hardcoded
    msg = can.Message(arbitration_id=0x15,data=[definitions.DATA_EE_PITCH2, out[0], out[1]],is_extended_id=False) 
    canbus.send(msg)


def ee_pitch2_list(dataa):
    global eez_val
    global eez_time

    act_time = time.time()
    eez_val += (filter_center(dataa.data)-512) * (act_time - eez_time)
    eez_val = interval(eez_val)
    eez_time = act_time

    out = int(eez_val).to_bytes(2, byteorder='little', signed=True)
    # ToDo at the moment address is hardcoded
    msg = can.Message(arbitration_id=0x15,data=[definitions.DATA_EE_PITCH2, out[0], out[1]],is_extended_id=False) 
    canbus.send(msg)


def ee_roll_list(dataa):
    global eex_val
    global eex_time

    act_time = time.time()
    eex_val += (filter_center(dataa.data)-512) * (act_time - eex_time)
    eex_val = interval(eex_val)
    eex_time = act_time

    out = int(eex_val).to_bytes(2, byteorder='little', signed=True)
    # ToDo at the moment address is hardcoded
    msg = can.Message(arbitration_id=0x15,data=[definitions.DATA_EE_ROLL, out[0], out[1]],is_extended_id=False) 
    canbus.send(msg)


if __name__ == '__main__':
    try:
        rospy.init_node('communication')
        rospy.loginfo("Hello! communication node started!")

        canbus = can.interface.Bus(channel='can0', bustype='socketcan')

        rospy.Subscriber("motor_topic",Motor,motor_list)
        rospy.Subscriber("eex",UInt16,ee_roll_list)
        rospy.Subscriber("eey",UInt16,ee_pitch_list)
        rospy.Subscriber("eez",UInt16,ee_pitch2_list)
        rospy.Subscriber("pitch",UInt16,pitch_list)

        rospy.spin()

    except rospy.ROSInterruptException:
        pass

