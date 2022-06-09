#!/usr/bin/env python3

import rospy
import constant as const
from ReseQROS.msg import Remote, Motor

# Dati in ingresso le coordinate del telecomando calcola i valori di riferimento usando le formule proposte
def calcolo_valori(remote_data):
    global motor_msg
    global pub

    #dati letti sul topic remote_control

    #ToDo check riscalamento
    velocita = remote_data.vel_avanzamento
    curvatura = remote_data.curvatura

    vsx = int(velocita*(1-curvatura))
    vdx = int(velocita*curvatura)
    angle = int(2*(curvatura-0.5)*const.ANGLE_MAX)
    

    #pubblicazione dati
    motor_msg.vdx = vdx
    motor_msg.vsx = vsx
    motor_msg.angle = angle
    motor_msg.address = const.ADDRESSES[0]

    pub.publish(motor_msg)

    return vdx, vsx, angle

#legge i comandi di alto livello sul topic custom_chatter e
#applica la funzione assegnazione_velocità se sono disponibili dati sul topic custom_chatter
def listener():
	rospy.Subscriber("remote_topic",Remote,calcolo_valori) # nome topic da cambiare

def main_function():
    global pub
    global motor_msg

	rospy.init_node('agevar')
    #definizione variabili strutturate per ROS
    pub=rospy.Publisher("motor_topic",Motor,queue_size=10)
    motor_msg=Motor() #Motor.msg={vdx,vsx,angle}

	rospy.loginfo("Hello! agevar node started!")
	listener()

if __name__ == '__main__':
    try:
		main_function()
	except rospy.ROSInterruptException:
		pass
