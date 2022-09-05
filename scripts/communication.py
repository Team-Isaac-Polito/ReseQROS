#!/usr/bin/python

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

if __name__ == '__main__':
	try:
		rospy.init_node('communication')
		rospy.loginfo("Hello! communication node started!")

		canbus = can.interface.Bus(channel='can0', bustype='socketcan')

		rospy.Subscriber("motor_topic",Motor,motor_list)

		rospy.spin()

	except rospy.ROSInterruptException:
		pass

