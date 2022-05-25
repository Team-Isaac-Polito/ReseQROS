#!/usr/bin/env python3

import rospy
from ReseQROS.msg import Remote, Motor
import constant as const
import math

'''
MODULO 1:
Input: phid1, v1

Output:
phi1 -> integrale discreto di phid1
xd1 = cos(phi1) * v1
yd1 = sin(phi1) * v1
x1 -> integrale discreto di xd1
y1 -> integrale discreto di yd1

MODULO i-esimo:
... #TODO
... 
...

@Riccardo Giacchino [301168] e @Marco Barbon [287462]
'''


Ts_joystick = 1/const.JOYSTICK_FREQ #la frequenza scelta è del tutto casuale, non è quella vera

# Liste
phi1 = [0]  # Lista in cui vengono memorizzati tutti i valori di phi_1, in questo caso serve solo per il plot, come
            # per le altre liste, può essere sostituita da una semplice variabile per memorizzare solo il valore al
            # tempo k e calcolare quello al tempo k+1
phid1=[]
x1 = [0]
y1 = [0]
xd1=[]
yd1=[]
v1=[]

def integrale_discreto(x,dx): # Funzione che esegue l'integrale discreto secondo la formula: x(k+1) = x(k) + dx(k)*Ts
    global Ts_joystick
    new_value = x[-1]+dx[-1]*Ts_joystick
    x.append(new_value)

def velocità_lineari(xd1, yd1, phi1, v1):
    xd1_new_value = math.cos(phi1[-1])*v1[-1]
    xd1.append(xd1_new_value)
    yd1_new_value = math.sin(phi1[-1])*v1[-1]
    yd1.append(yd1_new_value)
    return xd1, yd1

def velocità_motori(ang_vel,lin_vel):
    wdx = (lin_vel[-1]+ang_vel[-1]*const.d/2)/const.r
    wsx = (lin_vel[-1]-ang_vel[-1]*const.d/2)/const.r
    wi = 0
    return wdx, wsx, wi

def agevar_module_1(ang_vel, lin_vel):
    global phi1, phid1, x1, y1, xd1, yd1, v1

    phid1.append(ang_vel)
    v1.append(lin_vel)

    integrale_discreto(phi1, phid1)   # Calcolo di phi1
    velocità_lineari(xd1, yd1, phi1, v1) # Calcolo xd1 e yd1
    integrale_discreto(x1, xd1)  # Calcolo di x1
    integrale_discreto(y1, yd1)  # Calcolo di y1
    rospy.loginfo("phi1: %f, phid1: %f, x1: %f, y1: %f, xd1: %f, yd1: %f, v1: %f" % (phi1[-1], phid1[-1], x1[-1], y1[-1], xd1[-1], yd1[-1], v1[-1]))
    #TODO da togliere rospy.loginfo

    wdx, wsx, wi = velocità_motori(phid1,v1)

    return wdx, wsx, wi

# Riceve i dati dal topic "remote_control" di velocità e curvatura, li elabora e tramette i valori ottenuti 
# di velocità dei motori sul topic "motor_topic"
# La funzione viene richiamata come callback della funzione listener non appena sono disponibili dei nuovi dati sul topic "remote_control"
def assegnazione_velocità(remote_data):

    # definizione variabili strutturate per ROS
    pub=rospy.Publisher("motor_topic",Motor,queue_size=10)
    motor_msg=Motor() #Motor.msg={wdx,wsx,wi}

    # dati letti sul topic remote_control
    lin_vel = remote_data.vel_avanzamento
    ang_vel = remote_data.curvatura

    # calcola i valori wdx, wsx, wi iterativamente per ogni modulo e li trasmette su topic "motor_msg"                                
    for i in range(1,const.N_MOD+1):
        if i==1:
            wdx, wsx, wi = agevar_module_1(ang_vel,lin_vel) # Modulo 1
        else:
            wdx, wsx, wi = agevar_module_i(ang_vel,lin_vel) # Modulo i-esimo, TODO agevar_module_i da scrivere
        rospy.loginfo("wdx: %f, wsx: %f, wi: %f" % (wdx, wsx, wi))

        motor_msg.wdx = int(wdx) #TODO float o int?
        motor_msg.wsx = int(wsx) #TODO float o int?
        motor_msg.wi = int(wi)   #TODO float o int?
        motor_msg.address = const.ADDRESSES[i]

        pub.publish(motor_msg)

# legge i comandi di alto livello dal topic "remote_topic" e
# applica la funzione assegnazione_velocità ai valori ricevuti
def listener():
    rospy.Subscriber("remote_topic",Remote,assegnazione_velocità)

def main_function():
	rospy.init_node('agevar') #inizializza il nodo "agevar"
	#rate = rospy.Rate(const.FREQ) #frecuency in hertz

	rospy.loginfo("Hello! agevar node started!")
	listener()
    
	rospy.spin()

	#while not rospy.is_shutdown():
	#	rospy.loginfo("agevar node working")
	#	listener()
	#	rate.sleep()

if __name__ == '__main__':
	try:
		main_function()
	except rospy.ROSInterruptException:
		pass

# TODO: Provare con lettura di dati da file, quindi creare anche un file contenente i valori e nominalo 'dati_in_input.dat'
# TODO: connettere il nodo ad un telecomando per testare il suo funzionamento
