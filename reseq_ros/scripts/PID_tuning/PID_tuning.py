#!/usr/bin/env python3

import rospy
from std_msgs.msg import UInt16, Float32
from reseq_ros.msg import Motor
import definitions
from math import pi
import matplotlib.pyplot as plt
import time
import csv
import can
import struct
w_measure_left=[]
w_measure_right=[]
wsx_reference=[]
wdx_reference=[]
Kp,Kd,Ki=0,0,0
flag_start=0

def plot():
    global w_measure_left, w_measure_right, wsx_reference, wdx_reference, Kp, Kd, Ki, flag_start

    flag_start=0

    _ , axs = plt.subplots(2)

    plt.suptitle('PID tuning')

    axs[0].plot(wsx_reference,'r',label='reference_left')
    axs[1].plot(wdx_reference,'r',label='reference_right')

    wsx_reference=wsx_reference[:500]
    wdx_reference=wdx_reference[:500]
    w_measure_left=w_measure_left[:500]
    w_measure_right=w_measure_right[:500]

    axs[0].plot(w_measure_left,'k',label=f'Kp={Kp} Kd={Kd} Ki={Ki}')
    axs[0].legend(fontsize='small')
    axs[1].plot(w_measure_right,'k',label=f'Kp={Kp} Kd={Kd} Ki={Ki}')
    axs[1].legend(fontsize='small')

    t=time.strftime("%Hh_%Mm_%Ss")
    plt.savefig(f'./fig_{t}')
    #plt.show()

def data_csv():
    global w_measure_left, w_measure_right, wsx_reference, wdx_reference, flag_start

    t=time.strftime("%Hh_%Mm_%Ss")

    wsx_reference=wsx_reference[:500]
    wdx_reference=wdx_reference[:500]
    w_measure_left=w_measure_left[:500]
    w_measure_right=w_measure_right[:500]

    with open(f'./data_{t}.csv', mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(wsx_reference)
        csv_writer.writerow(w_measure_left)
        csv_writer.writerow(wdx_reference)
        csv_writer.writerow(w_measure_right)

def callback_stop(dataa):
    plot()
    data_csv()

def callback_reference(dataa):
    global wsx_reference, wdx_reference, flag_start

    #time.sleep(1)

    flag_start=1

    value_sx=dataa.wsx/100 # [rpm]
    value_dx=dataa.wdx/100

    wsx_reference.append(value_sx)
    wdx_reference.append(value_dx)

def callback_measure_left(dataa):
    global w_measure_left, flag_start
    if flag_start == 1:
        value=dataa.data/100    # [rpm]
        w_measure_left.append(value)

def callback_measure_right(dataa):
    global w_measure_right, flag_start
    if flag_start == 1:
        value=dataa.data/100    # [rpm]
        w_measure_right.append(value)

def listener():
    rospy.Subscriber("w_measure_left",Float32,callback_measure_left)
    rospy.Subscriber("w_measure_right",Float32,callback_measure_right)
    rospy.Subscriber("motor_topic",Motor,callback_reference)
    rospy.Subscriber("flag",UInt16,callback_stop)

def publisher_K_PID():
    global Kp,Kd,Ki

    pub_Kp=rospy.Publisher("Kp_PID",Float32,queue_size=10)
    pub_Kd=rospy.Publisher("Kd_PID",Float32,queue_size=10)
    pub_Ki=rospy.Publisher("Ki_PID",Float32,queue_size=10)

    pub_Kp.publish(Kp)
    pub_Kd.publish(Kd)
    pub_Ki.publish(Ki)

def publisher():
    freq=100 # Hz
    Ts=1/freq

    pub_motor=rospy.Publisher("motor_topic",Motor,queue_size=10)
    motor_msg=Motor() #Motor.msg={wdx,wsx,angle}

    pub_flag=rospy.Publisher("flag",UInt16,queue_size=10)

    rate=rospy.Rate(freq)

    t=0
    T_tuning=5

    while not rospy.is_shutdown() and t<T_tuning:

        if 1<t<1.1:
            motor_msg.wdx = 5000 #centi_rpm
            motor_msg.wsx = 5000 #centi_rpm
            motor_msg.angle = 0
            motor_msg.address = 21
        else:
            motor_msg.wdx = 0
            motor_msg.wsx = 0
            motor_msg.angle = 0
            motor_msg.address = 21

        t+=Ts

        pub_motor.publish(motor_msg)

        rate.sleep()

    motor_msg.wdx = 0
    motor_msg.wsx = 0
    motor_msg.angle = 0
    motor_msg.address = 21
    pub_motor.publish(motor_msg)

    pub_flag.publish(1)

# Main function
def main_function():
    global Kp,Kd,Ki

    rospy.init_node('PID_tuning')
    rospy.loginfo("Hello! PID_tuning node started!")
    print('Inserisci i valori del PID prima di iniziare:')
    Kp=input('Kp: ')
    Kd=input('Kd: ')
    Ki=input('Ki: ')
    addr = 0x15

    canbus = can.interface.Bus(channel='can1', bustype='socketcan')
    data = list(struct.pack('f', float(Kp)))
    msg = can.Message(arbitration_id=int(addr),data=[definitions.DATA_PID_KP]+data,is_extended_id=False)
    canbus.send(msg)

    data = list(struct.pack('f', float(Ki)))
    msg = can.Message(arbitration_id=int(addr),data=[definitions.DATA_PID_KI]+data,is_extended_id=False)
    canbus.send(msg)

    data = list(struct.pack('f', float(Kd)))
    msg = can.Message(arbitration_id=int(addr),data=[definitions.DATA_PID_KD]+data,is_extended_id=False)
    canbus.send(msg)


    publisher_K_PID()
    listener()
    publisher()
    rospy.spin()

if __name__ == '__main__':
        try:
                main_function()
        except rospy.ROSInterruptException:
                pass