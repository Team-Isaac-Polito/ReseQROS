#!/usr/bin/python

import definitions
import can
import os
import time
import rospy
import socket
from ReseQROS.msg import Motor
from std_msgs.msg import UInt16

HOST = '1.2.3.4'
PORT = 4242

def writeNumbers(addr, vsx, vdx, angle):
    addrb = addr.to_bytes(2, byteorder='little', signed=True)
    out = addrb

    vsxb = vsx.to_bytes(2, byteorder='little', signed=True)
    out += vsxb

    vdxb = vdx.to_bytes(2, byteorder='little', signed=True)
    out += vdxb

    angb = angle.to_bytes(2, byteorder='little', signed=True)
    out += angb

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(out)
        s.close()

def motor_list(dataa):
	writeNumbers(int(dataa.address),int(dataa.wsx),int(dataa.wdx),int(dataa.angle))
	#rospy.loginfo("received curv")

if __name__ == '__main__':
	try:
		rospy.init_node('communication')
		rospy.loginfo("Hello! communication node started!")

		rospy.Subscriber("motor_topic",Motor,motor_list)

		rospy.spin()

	except rospy.ROSInterruptException:
		pass

