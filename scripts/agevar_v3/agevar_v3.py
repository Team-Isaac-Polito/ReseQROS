#!/usr/bin/env python3

import rospy
from ReseQROS.msg import Remote, Motor
import tf
import constant as const
import math
import numpy as np

'''
vel_motors:
# TODO

kinematic:
# TODO

@Riccardo Giacchino [301168] e @Marco Barbon [287462]
'''

"""Constanti globali"""

Ts = 1/const.FREQ # Frequenza di iterazione dell'algoritmo, da scegliere e implementare con ROS


"""Funzioni per il calcolo delle variabili d'interesse"""

# calcola i valori di velocità lineare e angolare del modulo successivo a partire dagli stessi valori del modulo precedente
def kinematic(lin_vel_in,ang_vel_in):

    # TODO ...

    return lin_vel_out, ang_vel_out


# calcola wdx,wsx,wi in funzione della velocità lineare e angolare del modulo 
def vel_motors(lin_vel,ang_vel):

    # TODO ...

    return wdx, wsx, angle


"""Struttura ROS"""
# calcola il valore della velocità angolare del primo modulo a partire dalla curvatura desiderata
def curv2ang(curv):

    return ang_vel

# scala i valori in ingresso dal topic "remote_topic" da 0/1023 a -Vmax/Vmax
# e filtra le vibrazioni sulla posizione di riposo
def scalatura_in(lin_vel_in,curv_in):
    lin_vel_out = 512 if 462 < lin_vel_in < 562 else lin_vel_in # filtra le vibrazioni sulla posizione a riposo del joystick
    curv_out = 512 if 462 < curv_in < 562 else curv_in

    lin_vel_out = lin_vel_out-512 # da 0/1023 a -512/511
    curv_out = curv_out-512

    lin_vel_out = (lin_vel_out/512)*const.Max_Lin_vel # da -512/511 a -Max_Lin_vel/Max_Lin_vel
    curv_out = (curv_out/512)*const.Max_Curv_vel # da -512/511 a -Max_Curv_vel/Max_Curv_vel

    return lin_vel_out, curv_out

# Elabora e pubblica le velocità di rotazione dei motori di avanzamento (wdx,wsx) e imbardata (wi) di ogni modulo.
# La funzione viene richiamata come callback della funzione listener non appena sono disponibili dei nuovi dati sul topic "remote_control"
def assegnazione_velocità(remote_data):

    # scalatura
    lin_vel,curv = scalatura_in(remote_data.lin_vel,remote_data.curv)

    # da curvatura a velocità angolare
    ang_vel=curv2ang(curv)

    # definizione variabili strutturate per ROS
    pub=rospy.Publisher("motor_topic",Motor,queue_size=10)
    motor_msg=Motor() #Motor.msg={wdx,wsx,angle}

    # per ogni modulo ...                        
    for num_module in range(const.N_MOD):

        wdx, wsx, angle = vel_motors(lin_vel,ang_vel) # ... calcola wdx,wsx,wi in funzione della velocità lineare e angolare del modulo 
        motor_msg.wdx = int(wdx) 
        motor_msg.wsx = int(wsx) 
        motor_msg.angle = int(angle)
        motor_msg.address = const.ADDRESSES[num_module] 
        pub.publish(motor_msg) # ... tramette i valori wdx,wsx,angle sul topic "motor_topic"

        if num_module != range(const.N_MOD)[-1]: # per tutti i moduli tranne l'ultimo ...
            lin_vel,ang_vel = kinematic(lin_vel,ang_vel) # ... calcola i valori di velocità lineare e angolare del modulo successivo a partire dagli stessi valori del modulo precedente

# riceve i valori di velocità lineare e velocità angolare del primo modulo dal topic "remote_topic" e
# applica la funzione assegnazione_velocità ai valori ricevuti
def listener():
    rospy.Subscriber("remote_topic",Remote,assegnazione_velocità)

def main_function():

    rospy.init_node('agevar') #inizializza il nodo "agevar"
    rospy.loginfo("Hello! agevar node started!")

    #listener()
    #rospy.spin()

    rate = rospy.Rate(const.FREQ) #frecuency in hertz
    while not rospy.is_shutdown():
        rospy.loginfo("agevar node working")
        listener()
        rate.sleep()

if __name__ == '__main__':
	try:
		main_function()
	except rospy.ROSInterruptException:
		pass

# TODO: aggiungere equazioni nuove
# TODO: test funzionamento
