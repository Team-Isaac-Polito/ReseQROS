#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32, UInt8
from reseq_ros.msg import Real_input, Real_output, Real_motor

import matplotlib.pyplot as plt
import numpy as np

w_measure_head_right = []
w_measure_head_left = []
yaw_angle_head = []

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

real_output_0_lin_vel = []
real_output_0_ang_vel = []

real_output_1_lin_vel = []
real_output_1_ang_vel = []

real_output_2_lin_vel = []
real_output_2_ang_vel = []

def plot(title='',topics=[],csv=0): # topic=['lin_vel','ang_vel','w_L','w_L_meas','w_R','w_R_meas','yaw_meas']
    values = [globals()[topic] for topic in topics]

    fig, axs = plt.subplots(2,3,sharex=True)

    fig.suptitle(title)

    N = [len(value) for value in values]
    t_sim = 6
    t = [list(np.linspace(0,t_sim,num=n)) for n in N]

    axs[0,0].plot(t[0],values[0],color='black')
    axs[0,0].set_ylabel('lin_vel [m/s]')
    axs[0,0].set_xlabel('t [s]')

    axs[1,0].plot(t[1],values[1],color='black')
    axs[1,0].set_ylabel('ang_vel [rad/s]')
    axs[1,0].set_xlabel('t [s]')

    axs[0,1].plot(t[2],values[2],color='green',label='w_L')
    axs[0,1].plot(t[4],values[4],color='orange',label='w_R')
    axs[0,1].set_ylabel('w motors (references) [rpm]')
    axs[0,1].set_xlabel('t [s]')
    axs[0,1].legend()

    axs[1,1].plot(t[6],values[6],color='black')
    axs[1,1].set_ylabel('yaw mesured [°]')
    axs[1,1].set_xlabel('t [s]')
    axs[1,1].legend()

    axs[0,2].plot(t[2],values[2],color='red',label='reference')
    axs[0,2].plot(t[3],values[3],color='black',label='measured')
    axs[0,2].set_ylabel('w_L [rpm]')
    axs[0,2].set_xlabel('t [s]')
    axs[0,2].legend()

    axs[1,2].plot(t[4],values[4],color='red',label='reference')
    axs[1,2].plot(t[5],values[5],color='black',label='measured')
    axs[1,2].set_ylabel('w_R [rpm]')
    axs[1,2].set_xlabel('t [s]')
    axs[1,2].legend()

def callback_Float32(dataa, var):
    global real_motor_0_wdx

    meas = dataa.data

    if len(real_motor_0_wdx)>=1:
        if var == 'yaw_angle_middle' or var == 'yaw_angle_tail':
            if meas>180:
                meas=-360+meas
            globals()[var].append(meas) # [°]
        else:
            globals()[var].append(2*meas/100) # [rpm] 2x DA TOGLIEREEEEEE!!!


def callback_Real_motor(dataa,var):
    globals()[var+'_wdx'].append(-dataa.wdx*60/(2*np.pi)) # [rpm]
    globals()[var+'_wsx'].append(-dataa.wsx*60/(2*np.pi)) # [rpm]
    globals()[var+'_angle'].append(dataa.angle)

def callback_Real_output(dataa,var):
    globals()[var+'_lin_vel'].append(dataa.lin_vel) # [m/s]
    globals()[var+'_ang_vel'].append(dataa.ang_vel) # [rad/s]

def listener():

    subs = [rospy.Subscriber('w_measure_head_left',Float32,callback_Float32,'w_measure_head_left'),
            rospy.Subscriber('w_measure_head_right',Float32,callback_Float32,'w_measure_head_right'),

            rospy.Subscriber('w_measure_middle_left',Float32,callback_Float32,'w_measure_middle_left'),
            rospy.Subscriber('w_measure_middle_right',Float32,callback_Float32,'w_measure_middle_right'),
            rospy.Subscriber('yaw_angle_middle',Float32,callback_Float32,'yaw_angle_middle'),

            rospy.Subscriber('w_measure_tail_left',Float32,callback_Float32,'w_measure_tail_left'),
            rospy.Subscriber('w_measure_tail_right',Float32,callback_Float32,'w_measure_tail_right'),
            rospy.Subscriber('yaw_angle_tail',Float32,callback_Float32,'yaw_angle_tail'),

            rospy.Subscriber('real_motor_0',Real_motor,callback_Real_motor,'real_motor_0'),
            rospy.Subscriber('real_motor_1',Real_motor,callback_Real_motor,'real_motor_1'),
            rospy.Subscriber('real_motor_2',Real_motor,callback_Real_motor,'real_motor_2'),

            rospy.Subscriber('real_output_0',Real_output,callback_Real_output,'real_output_0'),
            rospy.Subscriber('real_output_1',Real_output,callback_Real_output,'real_output_1'),
            rospy.Subscriber('real_output_2',Real_output,callback_Real_output,'real_output_2')]

    rospy.sleep(10)

    [sub.unregister() for sub in subs]

    plot('MODULE 1',['real_output_0_lin_vel', 'real_output_0_ang_vel', 'real_motor_0_wsx', 'w_measure_head_left', 'real_motor_0_wdx', 'w_measure_head_right','yaw_angle_head'])
    plot('MODULE 2',['real_output_1_lin_vel', 'real_output_1_ang_vel', 'real_motor_1_wsx', 'w_measure_middle_left', 'real_motor_1_wdx', 'w_measure_middle_right','yaw_angle_middle'])
    plot('MODULE 3',['real_output_2_lin_vel', 'real_output_2_ang_vel', 'real_motor_2_wsx', 'w_measure_tail_left', 'real_motor_2_wdx', 'w_measure_tail_right','yaw_angle_tail'])    
    plt.show()

    rospy.spin()

if __name__ == '__main__':
    try:
        rospy.init_node('plot_test')
        rospy.loginfo("Hello! plot_test node started!") 
        listener()
        
    except rospy.ROSInterruptException:
        pass