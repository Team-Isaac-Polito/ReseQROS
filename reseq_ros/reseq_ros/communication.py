#!/usr/bin/python3

import reseq_ros.definitions as definitions
import can
import os
import time
import struct
import rclpy
from reseq_msgs.msg import Motor
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
	dataa.wsx = dataa.wsx*-10
	dataa.wdx = dataa.wdx*-10

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
		msg.data = float(val[0])
		tracLeftHeadPub.publish(msg)
	elif mess.data[0] == definitions.SEND_TRACTION_RIGHT_SPEED_HEAD:
		msg = Float32()
		val = struct.unpack('f',bytearray([mess.data[4],mess.data[3],mess.data[2],mess.data[1]]))
		msg.data = float(val[0])
		tracRightHeadPub.publish(msg)

	elif mess.data[0] == definitions.SEND_TRACTION_LEFT_SPEED_MIDDLE:
		msg = Float32()
		val = struct.unpack('f',bytearray([mess.data[4],mess.data[3],mess.data[2],mess.data[1]]))
		msg.data = float(val[0])
		tracLeftMiddlePub.publish(msg)
	elif mess.data[0] == definitions.SEND_TRACTION_RIGHT_SPEED_MIDDLE:
		msg = Float32()
		val = struct.unpack('f',bytearray([mess.data[4],mess.data[3],mess.data[2],mess.data[1]]))
		msg.data = float(val[0])
		tracRightMiddlePub.publish(msg)

	elif mess.data[0] == definitions.SEND_TRACTION_LEFT_SPEED_TAIL:
		msg = Float32()
		val = struct.unpack('f',bytearray([mess.data[4],mess.data[3],mess.data[2],mess.data[1]]))
		msg.data = float(val[0])
		tracLeftTailPub.publish(msg)
	elif mess.data[0] == definitions.SEND_TRACTION_RIGHT_SPEED_TAIL:
		msg = Float32()
		val = struct.unpack('f',bytearray([mess.data[4],mess.data[3],mess.data[2],mess.data[1]]))
		msg.data = float(val[0])
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


def main(args=None):
	global canbus

	global tempPub
	global currLeftPub
	global currRightPub
	global tracLeftHeadPub
	global tracRightHeadPub
	global tracLeftMiddlePub
	global tracRightMiddlePub
	global tracLeftTailPub
	global tracRightTailPub
	global yawAngleMiddlePub
	global yawAngleTailPub

	rclpy.init(args=args)

	node = rclpy.create_node('communication')
	node.get_logger().info("Hello! communication node started!")

	canbus = can.interface.Bus(channel='can1', bustype='socketcan')

	motor_sub = node.create_subscription(Motor,"motor_topic",motor_list,10)
	twist_sub = node.create_subscription(Twist,"twist_joystick",twist_list,10)
	
	# definizione variabili strutturate per ROS
	tempPub=node.create_publisher(Float32,"temperature_topic",10)
	currLeftPub=node.create_publisher(UInt16,"current_left_topic",10)
	currRightPub=node.create_publisher(UInt16,"current_right_topic",10)

	tracLeftHeadPub=node.create_publisher(Float32,"w_measure_head_left",10)
	tracRightHeadPub=node.create_publisher(Float32,"w_measure_head_right",10)

	tracLeftMiddlePub=node.create_publisher(Float32,"w_measure_middle_left",10)
	tracRightMiddlePub=node.create_publisher(Float32,"w_measure_middle_right",10)

	tracLeftTailPub=node.create_publisher(Float32,"w_measure_tail_left",10)
	tracRightTailPub=node.create_publisher(Float32,"w_measure_tail_right",10)

	yawAngleMiddlePub=node.create_publisher(Float32,"yaw_angle_middle",10)
	yawAngleTailPub=node.create_publisher(Float32,"yaw_angle_tail",10)

	listener = can.Listener()
	listener.on_message_received = recv_data
	notifier = can.Notifier(canbus, [listener])

	rclpy.spin(node)


if __name__ == '__main__':
	main()
