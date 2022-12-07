#!/usr/bin/env python3

import rospy
from std_msgs.msg import UInt16, Float32
from ReseQROS.msg import Motor

from math import pi
import matplotlib.pyplot as plt

w_measure_left=[[]]
w_measure_right=[[]]
wsx_reference=[]
wdx_reference=[]
Kp,Kd,Ki=[],[],[]
flag_start=0
n=0

def plot():
    global w_measure_left, w_measure_right, wsx_reference, wdx_reference, Kp, Kd, Ki, flag_start, n
    fig , axs = plt.subplots(2)

    plt.suptitle('PID tuning')

    axs[0].plot(wsx_reference,'r',label='reference_left')
    axs[1].plot(wdx_reference,'r',label='reference_right')

    for i in range(n+1):
        w_measure_left_n=w_measure_left[i]
        w_measure_right_n=w_measure_right[i]

        colors=['k','b','m','g','y','v'] # max 6 iterartions

        axs[0].plot(w_measure_left_n,colors[i],label=f'Kp={Kp[i]} Kd={Kd[i]} Ki={Ki[i]}')
        axs[0].legend(fontsize='small')
        axs[1].plot(w_measure_right_n,colors[i],label=f'Kp={Kp[i]} Kd={Kd[i]} Ki={Ki[i]}')
        axs[1].legend(fontsize='small')

    plt.savefig(f'/home/isaac/catkin_ws/src/ReseQROS/scripts/PID_tuning/figures/fig')
    plt.show()


def callback_stop(dataa):
    global w_measure_left, w_measure_right, wsx_reference, wdx_reference, Kp, Kd, Ki, flag_start, n

    if dataa==1:
        flag_start=0

        Kp.append(input('Kd: '))
        Kd.append(input('Kp: '))
        Ki.append(input('Ki: '))
        print('\n')
        stop=input('continue? [Enter:yes /:no]')
        print('\n')

        if stop=='/':
            plot()
            #rospy.on_shutdown('stop_program')
        else:       
            n+=1
            w_measure_left.append([])
            w_measure_right.append([])

def callback_reference(dataa):
    global wsx_reference, wdx_reference, flag_start, n

    flag_start=1
    
    if n==0:
        value_sx=dataa.wsx/1023*130 # [rpm]
        value_dx=dataa.wdx/1023*130

        wsx_reference.append(value_sx)
        wdx_reference.append(value_dx)

def callback_measure_left(dataa):
    global w_measure_left, flag_start, n
    if flag_start == 1:
        value=dataa.data/1000
        w_measure_left[n].append(value) # [rpm]

def callback_measure_right(dataa):
    global w_measure_right, flag_start, n
    if flag_start == 1:
        value=dataa.data/1000
        w_measure_right[n].append(value) # [rpm]

def listener():
    rospy.Subscriber("w_measure_left",Float32,callback_measure_left)
    rospy.Subscriber("w_measure_right",Float32,callback_measure_right)
    rospy.Subscriber("motor_topic",Motor,callback_reference)
    rospy.Subscriber("flag",UInt16,callback_stop)
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