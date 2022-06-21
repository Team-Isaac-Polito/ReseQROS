#!/usr/bin/python

import definitions
import can
import os

import rospy
from ReseQROS.msg import Motor


def writeNumbers(addr,vsx,vdx,angle):
	a = vsx & 0xFF
	b = vsx>>8 & 0xFF
	msg = can.Message(arbitration_id=addr,data=[definitions.DATA_TRACTION_LEFT, a, b],is_extended_id=False)
	canbus.send(msg)

	a = vdx & 0xFF
	b = vdx>>8 & 0xFF
	msg = can.Message(arbitration_id=addr,data=[definitions.DATA_TRACTION_RIGHT, a, b],is_extended_id=False)
	canbus.send(msg)

	a = angle & 0xFF
	b = angle>>8 & 0xFF
	msg = can.Message(arbitration_id=addr,data=[definitions.DATA_YAW, a, b],is_extended_id=False)
	canbus.send(msg)


def invio_dati(data):
	rospy.loginfo("DataToSend:\nADDR: " + str(data.address) + "\nVSX: " + str(data.vsx) + "\nVDX: " + str(data.vdx) + "\nANGLE: " + str(data.angle))
	writeNumbers(data.address,int(data.vsx),int(data.vdx),int(data.angle))


def testloop():
	vsx = 512
	vdx = 512
	yaw = 512
	rate = rospy.Rate(5) # 5 Hz
	while 1:
		writeNumbers(21, vsx, vdx, yaw)
		writeNumbers(22, vsx, vdx, yaw)
		writeNumbers(23, vsx, vdx, yaw)
		rate.sleep()


if __name__ == '__main__':
	try:
		rospy.init_node('communication')
		rospy.loginfo("Hello! communication node started!")

		canbus = can.interface.Bus(channel='can0', bustype='socketcan')

		rospy.Subscriber("motor_topic",Motor,invio_dati)

		rospy.spin()


	except rospy.ROSInterruptException:
		pass
