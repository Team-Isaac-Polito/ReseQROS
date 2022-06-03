#!/usr/bin/env python

import rospy
from std_msgs.msg import UInt16
import smbus as smbus
import struct

data = [0,0]
using = 0
def writeNumbers(addr):
    global I2Cbus
    global using
    if using:
      return
    using = 1
    byteList = []
    byteList += list(struct.pack('f', 0)) #data[0] + (data[1]/1024 - .5)*data[0]))
    byteList += list(struct.pack('f', 0)) #data[0] - (data[1]/1024 - .5)*data[0]))
    byteList += list(struct.pack('f', 0))
    byteList.append(0)  # fails to send last byte over I2C, hence this needs to be added 
    I2Cbus.write_i2c_block_data(addr, byteList[0], byteList[1:12])
    using = 0




def vel_list(dataa):
	data[0] = dataa.data
	#writeNumbers(21)


def curv_list(dataa):
	data[1] = dataa.data
	writeNumbers(21)


if __name__ == '__main__':
	global I2Cbus
	try:
		I2Cbus = smbus.SMBus(1)

		rospy.init_node('communication')

		rospy.loginfo("Hello! communication node started!")

		rospy.Subscriber("vel",UInt16,vel_list)
		rospy.Subscriber("curv",UInt16,curv_list)


		rospy.spin()
		

	except rospy.ROSInterruptException:
		pass
