#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32, UInt8
from reseq_ros.msg import Real_input, Real_output, Real_motor

from time import sleep
import matplotlib.pyplot as plt
import numpy as np

w_measure_head_right = []
w_measure_head_left = []

real_motor_0_wdx = []
real_motor_0_wsx = []
real_motor_0_angle = [] # always 0

w_measure_middle_right = []
w_measure_middle_left = []
yaw_angle_middle = []

real_motor_1_wdx = []
real_motor_1_wsx = []
real_motor_1_angle = []

w_measure_tail_right = []
w_measure_tail_left = []
yaw_angle_tail = []

real_motor_2_wdx = []
real_motor_2_wsx = []
real_motor_2_angle = []

def plot():
    global w_measure_head_right, real_motor_0_wdx, w_measure_head_left, real_motor_0_wsx
    global w_measure_middle_right, real_motor_1_wdx, w_measure_middle_left, real_motor_1_wsx, yaw_angle_middle, real_motor_1_angle
    global w_measure_tail_right, real_motor_2_wdx, w_measure_tail_left, real_motor_2_wsx, yaw_angle_tail, real_motor_2_angle

    fig, axs = plt.subplots(3,1,sharex=True)

    fig.suptitle("1st Module")

    N = len(real_motor_0_wdx)
    t = list(np.linspace(0,6,num=N))

    Nmdx = len(w_measure_head_right)
    tmdx = list(np.linspace(0,6,num=Nmdx))

    Nmsx = len(w_measure_head_left)
    tmsx = list(np.linspace(0,6,num=Nmsx))

    axs[0].plot(t,real_motor_0_wdx,label='wdx')
    axs[0].plot(t,real_motor_0_wsx,label='wsx')
    axs[0].set_ylabel('w [rpm]')
    axs[0].legend()

    axs[1].plot(t,real_motor_0_wdx,label='ref')
    axs[1].plot(tmdx,w_measure_head_right,label='meas')
    axs[1].set_ylabel('dx')
    axs[1].legend()

    axs[2].plot(t,real_motor_0_wsx,label='ref')
    axs[2].plot(tmsx,w_measure_head_left,label='meas')
    axs[2].set_ylabel('sx')
    axs[2].set_xlabel('t [s]')
    axs[2].legend()

    plt.show()

    ''' ----------------------- '''

    fig, axs = plt.subplots(4,1,sharex=True)

    fig.suptitle("2nd Module")

    N1 = len(real_motor_1_wdx)
    t1 = list(np.linspace(0,6,num=N1))

    Nmdx1 = len(w_measure_middle_right)
    tmdx1 = list(np.linspace(0,6,num=Nmdx1))

    Nmsx1 = len(w_measure_middle_left)
    tmsx1 = list(np.linspace(0,6,num=Nmsx1))

    Nmy1 = len(yaw_angle_middle)
    tmy1 = list(np.linspace(0,6,num=Nmy1))

    axs[0].plot(t1,real_motor_1_wdx,label='wdx')
    axs[0].plot(t1,real_motor_1_wsx,label='wsx')
    axs[0].set_ylabel('w [rpm]')
    axs[0].legend()

    axs[1].plot(t1,real_motor_1_wdx,label='ref')
    axs[1].plot(tmdx1,w_measure_middle_right,label='meas')
    axs[1].set_ylabel('dx')
    axs[1].legend()

    axs[2].plot(t1,real_motor_1_wsx,label='ref')
    axs[2].plot(tmsx1,w_measure_middle_left,label='meas')
    axs[2].set_ylabel('sx')
    axs[2].legend()

    axs[3].plot(t1,real_motor_1_angle,label='ref')
    axs[3].plot(tmy1,yaw_angle_middle,label='meas')
    axs[3].set_ylabel('angle [°]')
    axs[3].set_xlabel('t [s]')
    axs[3].legend()

    plt.show()

    ''' ---------------- '''

    fig, axs = plt.subplots(4,1,sharex=True)

    fig.suptitle("3rd Module")

    N2 = len(real_motor_2_wdx)
    t2 = list(np.linspace(0,6,N2))

    Nmdx2 = len(w_measure_tail_right)
    tmdx2 = list(np.linspace(0,6,num=Nmdx2))

    Nmsx2 = len(w_measure_tail_left)
    tmsx2 = list(np.linspace(0,6,num=Nmsx2)) 

    Nmy2 = len(yaw_angle_tail)
    tmy2 = list(np.linspace(0,6,num=Nmy2)) 

    axs[0].plot(t2,real_motor_2_wdx,label='wdx')
    axs[0].plot(t2,real_motor_2_wsx,label='wsx')
    axs[0].set_ylabel('w [rpm]')
    axs[0].legend()

    axs[1].plot(t2,real_motor_2_wdx,label='ref')
    axs[1].plot(tmdx2,w_measure_tail_right,label='meas')
    axs[1].set_ylabel('dx')
    axs[1].legend()

    axs[2].plot(t2,real_motor_2_wsx,label='ref')
    axs[2].plot(tmsx2,w_measure_tail_left,label='meas')
    axs[2].set_ylabel('sx')
    axs[2].legend()

    axs[3].plot(t2,real_motor_2_angle,label='ref')
    axs[3].plot(tmy2,yaw_angle_tail,label='meas')
    axs[3].set_ylabel('angle [°]')
    axs[3].set_xlabel('t [s]')
    axs[3].legend()

    plt.show()

def callback_Float32(dataa, var):
    global real_motor_0_wdx
    if len(real_motor_0_wdx)>=1:
        globals()[var].append(dataa.data/100) # [rpm]

def callback_Real_motor(dataa,var):
    globals()[var+'_wdx'].append(-dataa.wdx*60/(2*np.pi)) # [rpm]
    globals()[var+'_wsx'].append(-dataa.wsx*60/(2*np.pi)) # [rpm]
    globals()[var+'_angle'].append(dataa.angle)

def listener():

    sub1=rospy.Subscriber('w_measure_head_left',Float32,callback_Float32,'w_measure_head_left')
    sub2=rospy.Subscriber('w_measure_head_right',Float32,callback_Float32,'w_measure_head_right')

    sub3=rospy.Subscriber('w_measure_middle_left',Float32,callback_Float32,'w_measure_middle_left')
    sub4=rospy.Subscriber('w_measure_middle_right',Float32,callback_Float32,'w_measure_middle_right')
    sub5=rospy.Subscriber('yaw_angle_middle',Float32,callback_Float32,'yaw_angle_middle')

    sub6=rospy.Subscriber('w_measure_tail_left',Float32,callback_Float32,'w_measure_tail_left')
    sub7=rospy.Subscriber('w_measure_tail_right',Float32,callback_Float32,'w_measure_tail_right')
    sub8=rospy.Subscriber('yaw_angle_tail',Float32,callback_Float32,'yaw_angle_tail')

    sub9=rospy.Subscriber('real_motor_0',Real_motor,callback_Real_motor,'real_motor_0')
    sub10=rospy.Subscriber('real_motor_1',Real_motor,callback_Real_motor,'real_motor_1')
    sub11=rospy.Subscriber('real_motor_2',Real_motor,callback_Real_motor,'real_motor_2')

    rospy.sleep(10)

    sub1.unregister()
    sub2.unregister()
    sub3.unregister()
    sub4.unregister()
    sub5.unregister()
    sub6.unregister()
    sub7.unregister()
    sub8.unregister()
    sub9.unregister()
    sub10.unregister()
    sub11.unregister()

    plot()

    rospy.spin()

if __name__ == '__main__':
    try:
        rospy.init_node('plot_test')
        rospy.loginfo("Hello! plot_test node started!") 
        listener()
        
    except rospy.ROSInterruptException:
        pass