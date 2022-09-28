#!/usr/bin/python3

import definitions
import can
import os
import time
import rospy
from ReseQROS.msg import Motor
from std_msgs.msg import UInt16

def writeNumbers(addr,vsx,vdx,angle):
	out = vsx.to_bytes(2, byteorder='little', signed=True)
	msg = can.Message(arbitration_id=addr,data=[definitions.DATA_TRACTION_LEFT, out[0], out[1]],is_extended_id=False)
	canbus.send(msg)

	out = vdx.to_bytes(2, byteorder='little', signed=True)
	msg = can.Message(arbitration_id=addr,data=[definitions.DATA_TRACTION_RIGHT, out[0], out[1]],is_extended_id=False)
	canbus.send(msg)

	out = angle.to_bytes(2, byteorder='little', signed=True)
	msg = can.Message(arbitration_id=addr,data=[definitions.DATA_YAW, out[0], out[1]],is_extended_id=False)
	canbus.send(msg)

def motor_list(dataa):
	writeNumbers(int(dataa.address),int(dataa.wsx),int(dataa.wdx),int(dataa.angle))
	#rospy.loginfo("received curv")


def ee_list(dataa):
	
    out = int(dataa.data).to_bytes(2, byteorder='little', signed=True)
    # ToDo at the moment address is hardcoded
    msg = can.Message(arbitration_id=0x15,data=[definitions.DATA_EE_PITCH, out[0], out[1]],is_extended_id=False) 
    canbus.send(msg)

	
def pitch_list(dataa):
	
    out = int(dataa.data).to_bytes(2, byteorder='little', signed=True)
    # ToDo at the moment address is hardcoded
    msg = can.Message(arbitration_id=0x17,data=[definitions.DATA_PITCH, out[0], out[1]],is_extended_id=False) 
    canbus.send(msg)

if __name__ == '__main__':
	try:
		rospy.init_node('communication')
		rospy.loginfo("Hello! communication node started!")

		canbus = can.interface.Bus(channel='can0', bustype='socketcan')

		rospy.Subscriber("motor_topic",Motor,motor_list)

		rospy.Subscriber("EE_topic",UInt16,ee_list)

		rospy.Subscriber("PITCH_can",UInt16,pitch_list)

		rospy.spin()

	except rospy.ROSInterruptException:
		pass

