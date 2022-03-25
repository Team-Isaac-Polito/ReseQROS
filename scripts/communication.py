#!/usr/bin/env python

import rospy
from ReseQROS.msg import Motor

def invio_dati(data):
	rospy.loginfo("DataToSend:\nADDR: " + str(data.address) + "\nVSX: " + str(data.vsx) + "\nVDX: " + str(data.vdx) + "\nANGLE: " + str(data.angle))


if __name__ == '__main__':
	try:
		rospy.init_node('communication')
		rate = rospy.Rate(50) #frecuency in hertz - should be the same as agevar node (or more(?)) 

		rospy.loginfo("Hello! communication node started!")

		rospy.Subscriber("motor_topic",Motor,invio_dati)

		rospy.spin()
		

	except rospy.ROSInterruptException:
		pass
