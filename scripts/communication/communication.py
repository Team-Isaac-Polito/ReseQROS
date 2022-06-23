#!/usr/bin/python

import definitions
import can
import os
import time
import rospy
from ReseQROS.msg import Motor

vel=0
curv=0
tempo = 0

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


def invio_dati():
	rospy.loginfo("DataToSend:\nADDR: " + str(data.address) + "\nVSX: " + str(data.vsx) + "\nVDX: " + str(data.vdx) + "\nANGLE: " + str(data.angle))
	global vel
	global curv
	rospy.loginfo("executing writenumbers - vel " + str(vel) + " - curv - " + str(curv))

	# filtro posizioe nulla
	velo = 512 if 462 < vel < 562 else vel
	curvo = 512 if 462 < curv < 562 else curv

	velo = velo - 512		#-512 +512
	curvo = curvo - 512		#-512 +512

	vsx,vdx = mappaDrive(velo,curvo)

	writeNumbers(21,int(vsx),int(vdx),int(0))
	writeNumbers(22,int(vsx),int(vdx),int(0))
	writeNumbers(23,int(vsx),int(vdx),int(0))

def mappaDrive(velo,curvo):
	vsx = velo + curvo/2
	vdx = velo - curvo/2
	return vsx,vdx

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



def vel_list(dataa):
	global vel
	global tempo
	vel = int(dataa.data)
#	rospy.loginfo("received vel")
#	rospy.loginfo("--vel " + str(vel) + "- curv " + str(curv))
	if time.time() - tempo > 0.1:
		tempo = time.time()
		invio_dati()


def curv_list(dataa):
	global curv
	global tempo
	curv = int(dataa.data)
	#rospy.loginfo("received curv")


if __name__ == '__main__':
	try:
		rospy.init_node('communication')
		rospy.loginfo("Hello! communication node started!")

		canbus = can.interface.Bus(channel='can0', bustype='socketcan')

		#rospy.Subscriber("motor_topic",Motor,invio_dati)
		rospy.Subscriber("vel",UInt16,vel_list)
		rospy.Subscriber("curv",UInt16,curv_list)

		rospy.spin()


	except rospy.ROSInterruptException:
		pass
