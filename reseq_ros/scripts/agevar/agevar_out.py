#!/usr/bin/env python3

import rospy
from reseq_ros.msg import Real_output
from reseq_ros.msg import Motor

from agevar_constant import *
from math import degrees

'''
OUTPUT PROCESSING:
Output scaling + Motor velocities
'''

"""subfunctions of agevar_out"""

# Takes into account the saturation of the commands
def saturation(wdx,wsx,angle):
    angle=degrees(angle)

    if angle > delta_max:
        angle = delta_max
    elif angle < -delta_max:
        angle = -delta_max

    if wdx > w_max:
        wdx = w_max
    elif wdx < -w_max:
        wdx = -w_max

    if wsx > w_max:
        wsx = w_max
    elif wsx < -w_max:
        wsx = -w_max

    return wdx, wsx, angle

# Scales the output values used to feed the topic "motor_topic" from the real values to 0/1023
def out_scaling(wdx,wsx):
    wdx=wdx/w_max # from -w_max/w_max to -1/1
    wdx=int(wdx*1023) # from -1/1 to -1023/1023

    wsx=wsx/w_max # from -w_max/w_max to 0/1
    wsx=int(wsx*1023) # from -1/1 to -1023/1023

    return wdx, wsx

# It computes wdx,wsx,angle from the linear and angular velocity of the module
def vel_motors(lin_vel,ang_vel):
    wdx = (lin_vel+ang_vel*d/2)/r_eq
    wsx = (lin_vel-ang_vel*d/2)/r_eq

    return wdx, wsx


''' ------------------------- '''


# Callback function
def callback(dataa):
    num_module = dataa.num_module
    sign = dataa.sign
    lin_vel = dataa.lin_vel
    ang_vel = dataa.ang_vel
    angle = dataa.delta

    wdx, wsx = vel_motors(lin_vel,ang_vel)
    wdx, wsx, angle = saturation(wdx,wsx,angle)
    wdx, wsx = out_scaling(wdx,wsx)

    if sign == 0:  # backward
        wsx, wdx = -wsx,-wdx

    pub = rospy.Publisher("motor_topic",Motor,queue_size=10)
    motor_msg = Motor()

    motor_msg.wdx = wdx
    motor_msg.wsx = wsx
    motor_msg.angle = angle
    motor_msg.address = address[num_module]
    pub.publish(motor_msg) # send the values of wdx,wsx,angle on the topic "motor_topic"

if __name__ == '__main__':
    try:
        rospy.init_node('agevar_out')
        rospy.loginfo("Hello! agevar_out node started!") 
        
        for i in range(N_mod):
            rospy.Subscriber("Real_output_module_"+str(i),Real_output,callback)

        rospy.spin()
    except rospy.ROSInterruptException:
        pass