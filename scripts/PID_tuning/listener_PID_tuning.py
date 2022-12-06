#!/usr/bin/env python3

import rospy
from std_msgs.msg import UInt16, Float32
from ReseQROS.msg import Motor

from math import pi
import matplotlib.pyplot as plt

w_measure_left=[]
w_measure_right=[]
wsx_reference=[]
wdx_reference=[]
Kp,Kd,Ki=None,None,None
flag_start=0

def callback_plot(dataa):
    global w_measure_left, w_measure_right, wsx_reference, wdx_reference, Kp, Kd, Ki, flag_start

    flag_start=0

    Kp = input('Kd: ')
    Kd = input('Kp: ')
    Ki = input('Ki: ')

    fig , axs = plt.subplots(2)

    plt.suptitle(f'Kp={Kp} Kd={Kd} Ki={Ki}')

    axs[0].plot(wsx_reference,'r',label='reference_left')
    axs[0].plot(w_measure_left,'k',label='measure_left')

    axs[1].plot(wdx_reference,'r',label='reference_right')
    axs[1].plot(w_measure_right,'k',label='measure_right')

    plt.savefig(f'/home/isaac/catkin_ws/src/ReseQROS/scripts/PID_tuning/figures/Kp_{Kp}_Kd_{Kd}_Ki_{Ki}')
    plt.show()

def callback_reference(dataa):
    global wsx_reference, wdx_reference, flag_start

    flag_start=1
    
    value_sx=dataa.wsx/1023*130 # [rpm]
    value_dx=dataa.wdx/1023*130

    wsx_reference.append(value_sx)
    wdx_reference.append(value_dx)

def callback_measure_left(dataa):
    global w_measure_left, flag_start
    if flag_start == 1:
        value=dataa.data/1000
        w_measure_left.append(value) # [rpm]

def callback_measure_right(dataa):
    global w_measure_right, flag_start
    if flag_start == 1:
        value=dataa.data/1000
        w_measure_right.append(value) # [rpm]

def listener():
    rospy.Subscriber("w_measure_left",Float32,callback_measure_left)
    rospy.Subscriber("w_measure_right",Float32,callback_measure_right)
    rospy.Subscriber("motor_topic",Motor,callback_reference)
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