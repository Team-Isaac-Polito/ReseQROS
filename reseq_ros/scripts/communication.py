#!/usr/bin/python3

import definitions
import can
import os
import time
import struct
import rospy
from reseq_ros.msg import Motor
from std_msgs.msg import UInt16, Float32
from geometry_msgs.msg import Twist


eex_val = 512
eey_val = 1023
eez_val = 512
pitch_val = 0 # ToDo check starting Value

last_time = time.time()

def interval(data):
	return data if 0 <= data <= 1023 else 1023 if data > 1023 else 0 

def motor_list(dataa):
	#RPM to centiRPM scaling
	dataa.wsx = dataa.wsx*100
	dataa.wdx = dataa.wdx*100

	out = int(dataa.wsx).to_bytes(2, byteorder='little', signed=True)
	msg = can.Message(arbitration_id=int(dataa.address),data=[definitions.DATA_TRACTION_LEFT, out[0], out[1]],is_extended_id=False)
	canbus.send(msg)

	out = int(dataa.wdx).to_bytes(2, byteorder='little', signed=True)
	msg = can.Message(arbitration_id=int(dataa.address),data=[definitions.DATA_TRACTION_RIGHT, out[0], out[1]],is_extended_id=False)
	canbus.send(msg)

	#out = int(dataa.angle).to_bytes(2, byteorder='little', signed=True)
	#msg = can.Message(arbitration_id=int(dataa.address),data=[definitions.DATA_YAW, out[0], out[1]],is_extended_id=False)
	#canbus.send(msg)

def twist_list(data):
	global pitch_val
	global eex_val
	global eey_val
	global eez_val

	global last_time

	act_time = time.time()
	dt = act_time - last_time
	
	#pitch
	pitch_val += data.linear.z * dt
	pitch_val = interval(pitch_val)
	
	#EE_pitch
	eey_val += data.angular.y * dt
	eey_val = interval(eey_val)

	#EE_pitch2
	eez_val += (data.angular.y*0.75 + data.angular.z) * dt
	eez_val = interval(eez_val)

	#EE_roll
	eex_val += data.angular.x * dt
	eex_val = interval(eex_val)

	last_time = act_time

	out = int(pitch_val).to_bytes(2, byteorder='little', signed=True)
	msg = can.Message(arbitration_id=0x17,data=[definitions.DATA_PITCH, out[0], out[1]],is_extended_id=False) 
	canbus.send(msg)

	out = int(eey_val).to_bytes(2, byteorder='little', signed=True)
	msg = can.Message(arbitration_id=0x15,data=[definitions.DATA_EE_PITCH, out[0], out[1]],is_extended_id=False) 
	canbus.send(msg)

	out = int(eez_val).to_bytes(2, byteorder='little', signed=True)
	msg = can.Message(arbitration_id=0x15,data=[definitions.DATA_EE_PITCH2, out[0], out[1]],is_extended_id=False) 
	canbus.send(msg)

	out = int(eex_val).to_bytes(2, byteorder='little', signed=True)
	msg = can.Message(arbitration_id=0x15,data=[definitions.DATA_EE_ROLL, out[0], out[1]],is_extended_id=False) 
	canbus.send(msg)

def recv_data(mess):
	global tracLeftPub
	global tracRightPub
	global currLeftPub
	global currRightPub

	if mess.data[0] == definitions.SEND_TEMPERATURE:
		msg = Float32()
		val = struct.unpack('f',bytearray([mess.data[1],mess.data[2],mess.data[3],mess.data[4]]))
		msg.data = val
		tempPub.publish(msg)
		
	elif mess.data[0] == definitions.SEND_TRACTION_LEFT_SPEED_HEAD:
		msg = Float32()
		val = struct.unpack('f',bytearray([mess.data[4],mess.data[3],mess.data[2],mess.data[1]]))
		msg.data = float(val[0])/100.0 #scale centiRPM to RPM
		tracLeftHeadPub.publish(msg)
	elif mess.data[0] == definitions.SEND_TRACTION_RIGHT_SPEED_HEAD:
		msg = Float32()
		val = struct.unpack('f',bytearray([mess.data[4],mess.data[3],mess.data[2],mess.data[1]]))
		msg.data = float(val[0])/100.0 #scale centiRPM to RPM
		tracRightHeadPub.publish(msg)

	elif mess.data[0] == definitions.SEND_TRACTION_LEFT_SPEED_MIDDLE:
		msg = Float32()
		val = struct.unpack('f',bytearray([mess.data[4],mess.data[3],mess.data[2],mess.data[1]]))
		msg.data = float(val[0])/100.0 #scale centiRPM to RPM
		tracLeftMiddlePub.publish(msg)
	elif mess.data[0] == definitions.SEND_TRACTION_RIGHT_SPEED_MIDDLE:
		msg = Float32()
		val = struct.unpack('f',bytearray([mess.data[4],mess.data[3],mess.data[2],mess.data[1]]))
		msg.data = float(val[0])/100.0 #scale centiRPM to RPM
		tracRightMiddlePub.publish(msg)

	elif mess.data[0] == definitions.SEND_TRACTION_LEFT_SPEED_TAIL:
		msg = Float32()
		val = struct.unpack('f',bytearray([mess.data[4],mess.data[3],mess.data[2],mess.data[1]]))
		msg.data = float(val[0])/100.0 #scale centiRPM to RPM
		tracLeftTailPub.publish(msg)
	elif mess.data[0] == definitions.SEND_TRACTION_RIGHT_SPEED_TAIL:
		msg = Float32()
		val = struct.unpack('f',bytearray([mess.data[4],mess.data[3],mess.data[2],mess.data[1]]))
		msg.data = float(val[0])/100.0 #scale centiRPM to RPM
		tracRightTailPub.publish(msg)




	elif mess.data[0] == definitions.SEND_YAW_ENCODER_MIDDLE:
		msg = Float32()
		val = struct.unpack('f',bytearray([mess.data[4],mess.data[3],mess.data[2],mess.data[1]]))
		msg.data = float(val[0])
		yawAngleMiddlePub.publish(msg)	
	elif mess.data[0] == definitions.SEND_YAW_ENCODER_TAIL:
		msg = Float32()
		val = struct.unpack('f',bytearray([mess.data[4],mess.data[3],mess.data[2],mess.data[1]]))
		msg.data = float(val[0])
		yawAngleTailPub.publish(msg)

if __name__ == '__main__':
	try:
		rospy.init_node('communication')
		rospy.loginfo("Hello! communication node started!")

		canbus = can.interface.Bus(channel='can1', bustype='socketcan')

		rospy.Subscriber("motor_topic",Motor,motor_list)
		rospy.Subscriber("twist_joystick",Twist,twist_list)
		
		# definizione variabili strutturate per ROS
		tempPub=rospy.Publisher("temperature_topic",Float32,queue_size=10)
		currLeftPub=rospy.Publisher("current_left_topic",UInt16,queue_size=10)
		currRightPub=rospy.Publisher("current_right_topic",UInt16,queue_size=10)

		tracLeftHeadPub=rospy.Publisher("w_measure_head_left",Float32,queue_size=10)
		tracRightHeadPub=rospy.Publisher("w_measure_head_right",Float32,queue_size=10)

		tracLeftMiddlePub=rospy.Publisher("w_measure_middle_left",Float32,queue_size=10)
		tracRightMiddlePub=rospy.Publisher("w_measure_middle_right",Float32,queue_size=10)

		tracLeftTailPub=rospy.Publisher("w_measure_tail_left",Float32,queue_size=10)
		tracRightTailPub=rospy.Publisher("w_measure_tail_right",Float32,queue_size=10)

		yawAngleMiddlePub=rospy.Publisher("yaw_angle_middle",Float32,queue_size=10)
		yawAngleTailPub=rospy.Publisher("yaw_angle_tail",Float32,queue_size=10)
		
		listener = can.Listener()
		listener.on_message_received = recv_data
		notifier = can.Notifier(canbus, [listener])

		
		rospy.spin()

	except rospy.ROSInterruptException:
		pass

