#!/usr/bin/env python

import rospy


def talker():
	rospy.init_node('agevar')
	rate = rospy.Rate(10) #frecuency in hertz

	rospy.loginfo("Hello! agevar node started!")

	while not rospy.is_shutdown():
		rospy.loginfo("agevar node working")
		#ToDo
		# - check if something to read on topic
		# - do calculation
		# - publish output data on topic
		rate.sleep()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
