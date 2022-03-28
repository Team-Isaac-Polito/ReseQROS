#!/usr/bin/env python

import rospy
from ReseQROS.msg import Motor
import smbus as smbus
import struct

def writeNumbers(addr,values):
    global I2Cbus
    byteList = []
    for value in values:
        byteList += list(struct.pack('f', value))
    byteList.append(0)  # fails to send last byte over I2C, hence this needs to be added 
    I2Cbus.write_i2c_block_data(addr, byteList[0], byteList[1:12])



def invio_dati(data):
	rospy.loginfo("DataToSend:\nADDR: " + str(data.address) + "\nVSX: " + str(data.vsx) + "\nVDX: " + str(data.vdx) + "\nANGLE: " + str(data.angle))
	#ToDo convert data to set of bytes
	values = [float(data.vsx),float(data.vdx),float(data.angle)]
	writeNumbers(data.address,values)


if __name__ == '__main__':
	global I2Cbus
	try:
		I2Cbus = smbus.SMBus(1)

		rospy.init_node('communication')

		rospy.loginfo("Hello! communication node started!")

		rospy.Subscriber("motor_topic",Motor,invio_dati)

		rospy.spin()
		

	except rospy.ROSInterruptException:
		pass
