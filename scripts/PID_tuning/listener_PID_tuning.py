#!/usr/bin/env python3

import rospy
from std_msgs.msg import UInt16, Float32

import matplotlib.pyplot as plt

w_measure_left=[]
w_measure_right=[]
w_reference=[]

def callback_plot(dataa):
    global w_measure_left, w_measure_right, w_reference

    plt.plot(w_reference,'k',label='reference')
    plt.plot(w_measure_left,'r',label='measure_left')
    plt.plot(w_measure_right,'b',label='measure_right')

    plt.show()

def callback_reference(dataa):
    global w_reference
    value=(512-dataa.data)/512*65 # [rpm]
    w_reference.append(value)

def callback_measure_left(dataa):
    global w_measure_left
    value=dataa.data/1000
    w_measure_left.append(value) # [rpm]

def callback_measure_right(dataa):
    global w_measure_right
    value=dataa.data/1000
    w_measure_right.append(value) # [rpm]

def listener():
    rospy.Subscriber("lin_vel",UInt16,callback_reference)
    rospy.Subscriber("w_measure_left",Float32,callback_measure_left)
    rospy.Subscriber("w_measure_right",Float32,callback_measure_right)
    rospy.Subscriber("flag",UInt16,callback_plot)
    rospy.spin()

# Main function 
def main_function():
    rospy.init_node('listener_PID_tuning')
    rospy.loginfo("Hello! listener_PID_tuning node started!") 
    listener()

if __name__ == '__main__':
	try:
		main_function()
	except rospy.ROSInterruptException:
		pass