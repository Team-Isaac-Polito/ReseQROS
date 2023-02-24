#!/usr/bin/env python3

import rospy

from reseq_ros.msg import Real_input
from reseq_ros.msg import Real_output
from std_msgs.msg import Float32

from agevar_constant import *
from agevar_kinematic import *

'''
@Marco Barbon [287462]
For further details see Agevar's Report
'''

"""Global constants"""
delta = [0]*N_mod
yaw_angle_middle = 0
yaw_angle_tail = 0

"""ROS structure"""

# Computes and publishes the rotation speed of the feed motors (wdx,wsx) and the yaw angle (delta) of every module
def callback(dataa):
    global delta, yaw_angle_middle, yaw_angle_tail

    # lin_vel, ang_vel and sign of the first module
    lin_vel = dataa.lin_vel
    ang_vel = dataa.ang_vel
    sign = dataa.sign
    delta_meas = [yaw_angle_middle,yaw_angle_tail]

    # definition of ROS publishers
    pub = [rospy.Publisher("real_output_"+str(i),Real_output,queue_size=10) for i in range(N_mod)]
    Real_output_msg = Real_output()

    # module vector
    module_vector= list(range(N_mod))

    if sign==0:
        module_vector.reverse() # backward

    # for every module...
    for num_module in module_vector:

        Real_output_msg.num_module = num_module
        Real_output_msg.sign = sign
        Real_output_msg.lin_vel = lin_vel
        Real_output_msg.ang_vel = ang_vel
        Real_output_msg.delta = delta[num_module]
        pub[num_module].publish(Real_output_msg)

        if num_module != module_vector[-1]: # for every module except the last one
            # kinematic calculations
            # for more details see agevar_kinematic.py
            lin_vel,ang_vel = agevar_kinematic(lin_vel,ang_vel,delta,delta_meas,num_module,sign)

def callback_float(dataa,var):
    globals()[var] = dataa.data      

# Receives the values of feed speed and curve radius of the first module from the remote controller
# on the topic Real_input every time new values are available and it uses them to run the callback
def listener():
    rospy.Subscriber("yaw_angle_middle",Float32,callback_float,"yaw_angle_middle")
    rospy.Subscriber("yaw_angle_tail",Float32,callback_float,"yaw_angle_tail")

    rospy.Subscriber("real_input",Real_input,callback) 
    rospy.spin()

# Main function 
def main_function():
    rospy.init_node('agevar_core')
    rospy.loginfo("Hello! agevar_core node started!") 
    listener() 

if __name__ == '__main__':
	try:
		main_function()
	except rospy.ROSInterruptException:
		pass
