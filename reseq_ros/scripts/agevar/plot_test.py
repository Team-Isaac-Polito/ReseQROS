#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32, UInt8
from reseq_ros.msg import Real_input, Real_output, Real_motor

from time import sleep
import matplotlib.pyplot as plt

real_motor_0_wdx = []
real_motor_0_wsx = []
real_motor_0_angle = []

w_measure_right = []
w_measure_left = [],
yaw_angle = []

real_motor_1_wdx = []
real_motor_1_wsx = []
real_motor_1_angle = []

real_motor_2_wdx = []
real_motor_2_wsx = []
real_motor_2_angle = []

def plot():
    global w_measure_right, real_motor_0_wdx, w_measure_left, real_motor_0_wsx, yaw_angle, real_motor_0_angle
    global w_measure_right, real_motor_1_wdx, w_measure_left, real_motor_1_wsx, yaw_angle, real_motor_1_angle
    global w_measure_right, real_motor_2_wdx, w_measure_left, real_motor_2_wsx, yaw_angle, real_motor_2_angle

    fig, axs = plt.subplots(2,1,sharex=True)

    fig.suptitle("Motor 0")

    #axs[0].plot(w_measure_right,label='measure')
    axs[0].plot(real_motor_0_wdx,label='wdx')
    axs[0].plot(real_motor_0_wsx,label='wsx')
    axs[0].set_ylabel('wdx')
    axs[0].set_ylabel('w')

    #axs[2].plot(yaw_angle,label='measure')
    axs[1].plot(real_motor_0_angle,label='angle')
    axs[1].set_ylabel('angle')

    ''' ---------------- '''

    fig, axs = plt.subplots(2,1,sharex=True)

    fig.suptitle("Motor 1")

    #axs[0].plot(w_measure_right,label='measure')
    axs[0].plot(real_motor_1_wdx,label='wdx')
    axs[0].plot(real_motor_1_wsx,label='wsx')
    axs[0].set_ylabel('wdx')
    axs[0].set_ylabel('w')

    #axs[2].plot(yaw_angle,label='measure')
    axs[1].plot(real_motor_1_angle,label='angle')
    axs[1].set_ylabel('angle')

    ''' ---------------- '''

    fig, axs = plt.subplots(2,1,sharex=True)

    fig.suptitle("Motor 2")

    #axs[0].plot(w_measure_right,label='measure')
    axs[0].plot(real_motor_2_wdx,label='wdx')
    axs[0].plot(real_motor_2_wsx,label='wsx')
    axs[0].set_ylabel('wdx')
    axs[0].set_ylabel('w')

    #axs[2].plot(yaw_angle,label='measure')
    axs[1].plot(real_motor_2_angle,label='angle')
    axs[1].set_ylabel('angle')

    plt.show()

def callback_Float32(dataa, var):
    globals()[var].append(dataa.data)

def callback_Real_motor(dataa,var):
    globals()[var+'_wdx'].append(dataa.wdx)
    globals()[var+'_wsx'].append(dataa.wsx)
    globals()[var+'_angle'].append(dataa.angle)

def listener():

    rospy.Subscriber('w_measure_left',Float32,callback_Float32,'w_measure_left')
    rospy.Subscriber('w_measure_right',Float32,callback_Float32,'w_measure_right')
    rospy.Subscriber('yaw_angle',Float32,callback_Float32,'yaw_angle')

    rospy.Subscriber('real_motor_0',Real_motor,callback_Real_motor,'real_motor_0')
    rospy.Subscriber('real_motor_1',Real_motor,callback_Real_motor,'real_motor_1')
    rospy.Subscriber('real_motor_2',Real_motor,callback_Real_motor,'real_motor_2')

    sleep(5)
    plot()

    rospy.spin()

if __name__ == '__main__':
    try:
        rospy.init_node('plot_test')
        rospy.loginfo("Hello! plot_test node started!") 
        listener()
        
    except rospy.ROSInterruptException:
        pass