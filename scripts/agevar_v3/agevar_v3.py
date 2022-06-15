#!/usr/bin/env python3

from tkinter.messagebox import NO

from pyrsistent import m
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

# Marco so che non ti piacerà, è una soluzione temporane, poi farò un lavoro migliore con la modalità che avevo detto,
# è solo che questa è quella più veloce per giovedì
theta = [0]*const.N_MOD
angular_vel = [0]*const.N_MOD
linear_vel = [0]*const.N_MOD



"""Funzioni per la scalatura"""

# calcola il valore della velocità angolare del primo modulo a partire dalla curvatura desiderata
def curv2ang(lin_vel,curv):
    ang_vel=lin_vel/curv

    if curv > (9/10)*const.Max_Curv: # quando il raggio di curvatura supera 9/10 del valore massimo, si suppone che il comando sia di andare a dritto senza curvare
        ang_vel=0

    return ang_vel

# scala i valori in ingresso dal topic "remote_topic" da 0/1023 a Valore_min/Valore_max
# e filtra le vibrazioni sulla posizione di riposo
def scalatura_in(lin_vel_in,curv_in):
    lin_vel_out = 512 if 462 < lin_vel_in < 562 else lin_vel_in # filtra le vibrazioni sulla posizione a riposo del joystick
    curv_out = 512 if 462 < curv_in < 562 else curv_in

    lin_vel_out = lin_vel_out-512 # da 0/1023 a -512/511
    lin_vel_out = (lin_vel_out/512)*const.Max_Lin_vel # da -512/511 a -Max_Lin_vel/Max_Lin_vel
    
    curv_out = const.Min_Curv+(curv_out/1023)*(const.Max_Curv-const.Min_Curv) # da 0/1023 a Min_Curv/Max_Curv

    return lin_vel_out, curv_out


"""Funzioni per il calcolo delle variabili d'interesse"""

# calcola i valori di velocità lineare e angolare del modulo successivo a partire dagli stessi valori del modulo precedente
def kinematic(lin_vel_in,ang_vel_in,module):

    theta_dot = -(1/const.b)*(angular_vel[module]*(const.b+const.a*math.cos(theta[module]))+linear_vel[module]*math
    .sin(theta[module]))
    theta[module]=theta[module]+theta_dot*Ts

    ang_vel_out = ang_vel_in + theta_dot

    lin_vel_out_x = lin_vel_in + const.b*math.sin(theta[module])*ang_vel_out
    lin_vel_out_y = -ang_vel_in*const.a - const.b*math.cos(theta[module])*ang_vel_out
    
    lin_vel_out = math.sqrt(lin_vel_out_x**2 + lin_vel_out_y**2)

    return lin_vel_out, ang_vel_out


# calcola wdx,wsx,wi in funzione della velocità lineare e angolare del modulo 
def vel_motors(lin_vel,ang_vel,module):

    wdx = (lin_vel+ang_vel*const.d/2)/const.r
    wsx = (lin_vel-ang_vel*const.d/2)/const.r
    angle = theta[module]

    return wdx, wsx, angle


"""Struttura ROS"""

# Elabora e pubblica le velocità di rotazione dei motori di avanzamento (wdx,wsx) e imbardata (wi) di ogni modulo.
# La funzione viene richiamata come callback della funzione listener non appena sono disponibili dei nuovi dati sul topic "remote_control"
def assegnazione_velocità(remote_data):

    # scalatura
    lin_vel,curv = scalatura_in(remote_data.lin_vel,remote_data.curv)

    # da curvatura a velocità angolare
    ang_vel=curv2ang(lin_vel,curv)

    # definizione variabili strutturate per ROS
    pub=rospy.Publisher("motor_topic",Motor,queue_size=10)
    motor_msg=Motor() #Motor.msg={wdx,wsx,angle}

    # per ogni modulo ...                        
    for num_module in range(const.N_MOD):

        wdx, wsx, angle = vel_motors(lin_vel,ang_vel,num_module) # ... calcola wdx,wsx,wi in funzione della velocità lineare e angolare del modulo 
        motor_msg.wdx = int(wdx) 
        motor_msg.wsx = int(wsx) 
        motor_msg.angle = int(angle)
        motor_msg.address = const.ADDRESSES[num_module] 
        pub.publish(motor_msg) # ... tramette i valori wdx,wsx,angle sul topic "motor_topic"

        if num_module != range(const.N_MOD)[-1]: # per tutti i moduli tranne l'ultimo ...
            lin_vel,ang_vel = kinematic(lin_vel,ang_vel,num_module) # ... calcola i valori di velocità lineare e angolare del modulo successivo a partire dagli stessi valori del modulo precedente

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
