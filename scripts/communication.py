#!/usr/bin/env python

import rospy


def talker():
	rospy.init_node('communication')
	rate = rospy.Rate(50) #frecuency in hertz - should be the same as agevar node (or more(?)) 

	rospy.loginfo("Hello! communication node started!")

	while not rospy.is_shutdown():
		rospy.loginfo("communication node working")
		#ToDo
		# - check if something to read on topic
		# - send data to pico

		rate.sleep()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
