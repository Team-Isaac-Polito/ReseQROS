#!/usr/bin/python3

import definitions
import can
import os
import time
import rospy
from reseq_ros.msg import Motor
from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist

canbus = can.interface.Bus(channel='can0', bustype='socketcan')

def motor_list(addr,sx,dx):
    out = int(sx).to_bytes(2, byteorder='little', signed=True)
    msg = can.Message(arbitration_id=int(addr),data=[definitions.DATA_TRACTION_LEFT, out[0], out[1]],is_extended_id=False)
    canbus.send(msg)

    out = int(dx).to_bytes(2, byteorder='little', signed=True)
    msg = can.Message(arbitration_id=int(addr),data=[definitions.DATA_TRACTION_RIGHT, out[0], out[1]],is_extended_id=False)
    canbus.send(msg)

    #out = int(dataa.angle).to_bytes(2, byteorder='little', signed=True)
    #msg = can.Message(arbitration_id=int(dataa.address),data=[definitions.DATA_YAW, out[0], out[1]],is_extended_id=False)
    #canbus.send(msg)
while 1:
    motor_list(0x15,300,300)
    #motor_list(0x16,300,300)
    #motor_list(0x17,300,300)
    time.sleep(0.1)
