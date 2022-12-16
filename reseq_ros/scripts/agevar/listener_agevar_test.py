#!/usr/bin/env python3

import rospy
from reseq_ros.msg import Topic_ref
from std_msgs.msg import UInt16, Float32

import matplotlib.pyplot as plt

measure=[]
reference=[]

def callback_plot(dataa):
    global measure, reference

    plt.plot(reference,'k',label='reference')
    plt.plot(measure,'r',label='measure')

    plt.show()

def callback_reference(dataa):
    global reference
    reference.append(dataa.data)

def callback_measure(dataa):
    global measure
    measure.append(dataa.data)

def listener():
    rospy.Subscriber("reference",Topic_ref,callback_reference) # da sostituire con valori di riferimento
    rospy.Subscriber("measure",Float32,callback_measure) # da sostituire con valori misurati
    rospy.Subscriber("flag",UInt16,callback_plot) # da sostituire con la flag di un bottone del telecomando
    rospy.spin()

# Main function
def main_function():
    rospy.init_node('listener_agevar_test')
    rospy.loginfo("Hello! listener_agevar_test node started!") 
    listener()

if __name__ == '__main__':
	try:
		main_function()
	except rospy.ROSInterruptException:
		pass
