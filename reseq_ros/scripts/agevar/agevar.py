#!/usr/bin/env python3

import rospy

from std_msgs.msg import UInt16
from reseq_ros.msg import Motor

from agevar_constant import *
from agevar_check import *
from agevar_in import *
from agevar_out import *
from agevar_kinematic import *

'''
@Riccardo Giacchino [301168] e @Marco Barbon [287462]
For further details see Agevar's Report
'''

"""Global constants"""
delta = [0]*N_mod
lin_vel=512
r_curv=512

"""ROS structure"""

# Computes and publishes the rotation speed of the feed motors (wdx,wsx) and the yaw angle (delta) of every module
def publisher(lin_vel,r_curv):
    global delta

    # definition of some ROS variables
    pub=rospy.Publisher("motor_topic",Motor,queue_size=10)
    motor_msg=Motor() #Motor.msg={wdx,wsx,angle}

    # input processing (filter + input scaling + direction of motion + angular velocity)
    # for more details see agevar_in.py
    sign,lin_vel,ang_vel=agevar_in(lin_vel,r_curv)

    # module vector
    if sign==1:
        module_vector= list(range(N_mod)) # forward
    else:
        module_vector= list(range(N_mod)) # backward
        module_vector.reverse()

    # for every module...
    for num_module in module_vector:

        # check_print1(num_module,module_vector,lin_vel,ang_vel)

        # output processing (output scaling + motor velocities)
        # for more details see agevar_out.py
        wdx,wsx,angle = agevar_out(num_module,sign,lin_vel,ang_vel,delta)

        check_print2(num_module,module_vector,wdx,wsx,angle)
        check_sim(num_module,lin_vel,ang_vel)

        motor_msg.wdx = wdx
        motor_msg.wsx = wsx
        motor_msg.angle = angle
        motor_msg.address = address[num_module]
        pub.publish(motor_msg) # send the values of wdx,wsx,angle on the topic "motor_topic"

        if num_module != module_vector[-1]: # for every module except the last one
            # kinematic calculations
            # for more details see agevar_kinematic.py
            lin_vel,ang_vel = agevar_kinematic(lin_vel,ang_vel,delta,num_module,sign) 


# Saves the new value of feed speed into the global variable lin_vel 
def lin_vel_callback(dataa):
    global lin_vel
    lin_vel=int(dataa.data)

# Saves the new value of curve radius into the global variable r_curv 
# and runs the publisher function with the new values  
def r_curv_callback(dataa):
    global r_curv, lin_vel
    r_curv=int(dataa.data)
    publisher(lin_vel,r_curv)

# Receives the values of feed speed and curve radius of the first module from the remote controller on the topics "lin_vel" and "r_curv" every time new values are available
# and uses them to run the callbacks (It needs two different callbacks to achieve synchronization between the two topics)
#TODO: change the name of the topics from (vel,curv) into (lin_vel,r_curv)
def listener():
    rospy.Subscriber("lin_vel",UInt16,lin_vel_callback)
    rospy.Subscriber("r_curv",UInt16,r_curv_callback)
    rospy.spin()

# Main function 
def main_function():
    rospy.init_node('agevar')  # initializzation of agevar node
    rospy.loginfo("Hello! agevar node started!") 
    listener() 

if __name__ == '__main__':
	try:
		main_function()
	except rospy.ROSInterruptException:
		pass
