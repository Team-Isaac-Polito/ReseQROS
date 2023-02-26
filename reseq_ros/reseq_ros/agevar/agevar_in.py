#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from reseq_ros.msg import Real_input

from agevar_constant import *

'''
INPUT PROCESSING:
Filter + Input scaling + Direction of motion + Angular velocity 
'''

"""subfunctions of agevar_in"""

# Filters the vibration around the resting position
def filter(lin_vel,r_curv):
    lin_vel = 0 if -50 < lin_vel < 50 else lin_vel
    r_curv = 0 if -50 < r_curv < 50 else r_curv
    return lin_vel, r_curv

# Scales the inputs from topic "twist_joystick" from 0/1023 to their real values
def in_scaling(lin_vel,r_curv):
    # lin_vel:
    lin_vel = -(lin_vel/512)*lin_vel_max # from -512/511 to lin_vel_max/-lin_vel_max

    # r_curv:
    if r_curv >= 0:
        r_curv = r_curv_max-(r_curv_max-r_curv_min)*r_curv/512 # from 0/511 to r_curv_max/r_curv_min
    else:
        r_curv = -r_curv_max-(r_curv_max-r_curv_min)*r_curv/512 # from -512/-1 to -r_curv_min/-r_curv_max
    return lin_vel, r_curv

# Computes the direction of the motion (forward or backward)
# and deals with backward motion's problems
def direction(lin_vel,r_curv):
    if lin_vel<0:
        # backward:
        # sign=0 for convention
        # we invert the sign of lin_vel and r_curv, in order to treat this case as a forward movement,
        # indeed to do this we think the robot as it was in the reverse configuration (where the last module is the first and the first one is the last).
        # thus lin_vel becomes positive and r_curv change direction
        return -lin_vel, -r_curv, 0
    else:
        # forward:
        # sign=1
        # we leave unchanged the sign of lin_vel and r_curv
        return lin_vel, r_curv, 1

# It computes the angular velocity from the radius of curvature
def r_curv2ang(lin_vel,r_curv):
    ang_vel=lin_vel/r_curv

    if r_curv == r_curv_max or r_curv == -r_curv_max: #if the radius of curvature achieve his maximum value then the robot has to proceed forward without steering
        ang_vel=0

    return ang_vel


""" --------------------------- """


# Callback function
def callback(dataa):
    lin_vel = dataa.linear.y
    r_curv = dataa.linear.x

    lin_vel,r_curv=filter(lin_vel,r_curv)
    lin_vel,r_curv = in_scaling(lin_vel,r_curv)
    lin_vel,r_curv,sign = direction(lin_vel,r_curv)
    ang_vel=r_curv2ang(lin_vel,r_curv)

    pub = rospy.Publisher("real_input",Real_input,queue_size=10)
    Real_input_msg = Real_input()
    Real_input_msg.lin_vel = lin_vel
    Real_input_msg.r_curv = r_curv
    Real_input_msg.ang_vel = ang_vel
    Real_input_msg.sign = sign

    pub.publish(Real_input_msg)

if __name__ == '__main__':
    try:
        rospy.init_node('agevar_in')
        rospy.loginfo("Hello! agevar_in node started!") 
        
        rospy.Subscriber("twist_joystick",Twist,callback)

        rospy.spin()
    except rospy.ROSInterruptException:
        pass