#!/usr/bin/env python

import rospy
from std_msgs.msg import UInt16
import smbus as smbus
import struct
import time

vel = 0
curv = 0

def writeNumbers(addr):
	global I2Cbus
	global vel
	global curv
	rospy.loginfo("executing writenumbers - vel " + str(vel) + " - curv - " + str(curv))

	# filtro posizioe nulla
	velo = 512 if 462 < vel < 562 else vel
	curvo = 512 if 462 < curv < 562 else curv

	velo = velo - 512		#-512 +512
	curvo = curvo - 512		#-512 +512


	if abs(velo) < 150:
		vsx,vdx = mappaPivot(velo,curvo)
	else:
		vsx,vdx = mappaDrive(velo,curvo)

	rospy.loginfo("calculated values - vsx " + str(vsx) + " - vdx - " + str(vdx))

#	rospy.loginfo("--vsx " + str(vsx) + "- vdx " + str(vdx))


	byteList = []
	byteList += list(struct.pack('f', float(vsx)))
	byteList += list(struct.pack('f', float(vdx)))
#	byteList += list(struct.pack('f', float(0)))
#	byteList.append(0)  # fails to send last byte over I2C, hence this needs to be added
#	rospy.loginfo("printing i2c: " + str(len(byteList)))
	I2Cbus.write_i2c_block_data(addr, byteList[0], byteList[1:])
	#rospy.loginfo("error")

def mappaPivot(velo,curvo):
	vsx = curvo/2
	vdx = -vsx
	return vsx, vdx
def mappaDrive(velo,curvo):
	vsx = velo + curvo/2
	vdx = velo - curvo/2
	return vsx,vdx

tempo = 0

def vel_list(dataa):
	global vel
	global tempo
	vel = int(dataa.data)
#	rospy.loginfo("received vel")
#	rospy.loginfo("--vel " + str(vel) + "- curv " + str(curv))
	if time.time() - tempo > 0.1:
		tempo = time.time()
		writeNumbers(21)


def curv_list(dataa):
	global curv
	global tempo
	curv = int(dataa.data)
	#rospy.loginfo("received curv")



if __name__ == '__main__':
	global I2Cbus
	try:
		I2Cbus = smbus.SMBus(1)

		rospy.init_node('communication')

		rospy.loginfo("Hello! communication node started!")
		rate = rospy.Rate(10) # 1 Hz
		rospy.Subscriber("vel",UInt16,vel_list)
		rospy.Subscriber("curv",UInt16,curv_list)

#		while 1:
#			writeNumbers(21)
#			rate.sleep()

		rospy.spin()


	except rospy.ROSInterruptException:
		pass
