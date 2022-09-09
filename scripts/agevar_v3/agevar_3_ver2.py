#!/usr/bin/env python3

import os
from pyexpat.errors import XML_ERROR_INCOMPLETE_PE
import rospy
from ReseQROS.msg import Remote, Motor
from std_msgs.msg import UInt16
#import tf
import constant as const
import math

'''
@Riccardo Giacchino [301168] e @Marco Barbon [287462]
'''

"""Constanti globali"""

# Marco so che non ti piacerà, è una soluzione temporane, poi farò un lavoro migliore con la modalità che avevo detto,
# è solo che questa è quella più veloce per giovedì
theta = [0]*const.N_MOD
vel=512
curv=512


"""Funzioni per la scalatura"""

# calcola il valore della velocità angolare del primo modulo a partire dalla curvatura desiderata
def curv2ang(lin_vel,curv):

    if curv == 'inf': # quando il raggio di curvatura è infinito il modulo procede dritto senza curvare
        ang_vel=0
    else:
        ang_vel=lin_vel/curv

    return ang_vel

def direzione_in(lin_vel,curv):
    if (lin_vel<0):
        if (curv=='inf'):
            return 0, -lin_vel, 'inf'
        else:
            return 0, -lin_vel, -curv
    else:
        return 1, lin_vel, curv

def direzione_out(wdx, wsx, angle, segno):
    if segno == 0: #retromarcia
        wdx,wsx=-wdx,-wsx
        #angle???
    return wdx, wsx, angle

# Filtra le vibrazioni sulla posizione di riposo.
# E scala i valori in ingresso dal topic "remote_topic":
# vel: 1023/0 => 0 / 462-562 / 1023 => -Max_Lin_vel (indietro) / 0 (fermo) / Max_Lin_vel (avanti)
# curv: 1023/0 => 0 / 461 / 462-562 / 563 / 1023 => -Min_Curv (dx) / -Max_curv (dx) / 'inf' (Dritto) / Max_curv (sx) / Min_Curv (sx)
def scalatura_in(lin_vel_in,curv_in):

    lin_vel_in=1023-lin_vel_in # da 1023/0 a 0/1023
    curv_in=1023-curv_in # da 1023/0 a 0/1023

    lin_vel_out = 512 if 462 <= lin_vel_in <= 562 else lin_vel_in # filtro
    lin_vel_out = lin_vel_out-512 # da 0/512/1023 a -512/0/511
    lin_vel_out = (lin_vel_out/512)*const.Max_Lin_Vel # da -512/0/511 a -Max_Lin_vel/0/Max_Lin_vel

    curv_out = 512 if 462 <= curv_in <= 562 else curv_in # filtro
    curv_out = curv_out-512 # da 0/512/1023 a -512/0/511
    if curv_out == 0:
        curv_out='inf' # da -50/50 a 'inf'
    elif curv_out > 0: 
        y_min=const.Min_Curv 
        y_max=const.Max_Curv
        x_min=51
        x_max=511
        x=curv_out
        '''
        AUMENTANDO IL GRADO DELLA FUNZIONE INTERPOLANTE SI AUMENTA LA SENSIBILITA' DEL POTENZIOMETRO PER VALORI VICINI ALLA POSIZIONE DI RIPOSO!
        E CONTEMPORANEMENTE SI DIMINUISCE LA SENSIBILITA' PER I VALORI ESTREMI
        y=y_min+(y_max-y_min)/(x_min-x_max)*(x-x_max)      # interpolazione lineare
        y=y_min+(y_max-y_min)/(x_min-x_max)**2*(x-x_max)**2 # interpolazione quadratica
        '''
        y=y_min+(y_max-y_min)/(x_min-x_max)**3*(x-x_max)**3 # interpolazione cubica        
        curv_out=y
    elif curv_out < 0:
        y_min=-const.Min_Curv 
        y_max=-const.Max_Curv
        x_min=-51
        x_max=-512
        x=curv_out
        '''
        AUMENTANDO IL GRADO DELLA FUNZIONE INTERPOLANTE SI AUMENTA LA SENSIBILITA' DEL POTENZIOMETRO PER VALORI VICINI ALLA POSIZIONE DI RIPOSO!
        E CONTEMPORANEMENTE SI DIMINUISCE LA SENSIBILITA' PER I VALORI ESTREMI
        y=y_min+(y_max-y_min)/(x_min-x_max)*(x-x_max)      # interpolazione lineare
        y=y_min+(y_max-y_min)/(x_min-x_max)**2*(x-x_max)**2 # interpolazione quadratica
        '''
        y=y_min+(y_max-y_min)/(x_min-x_max)**3*(x-x_max)**3 # interpolazione cubica        
        curv_out=y
    return lin_vel_out, curv_out

# scala i valori in uscita verso il topic "motor_topic" da Valore_min/Valore_max a 0/1023
# e impone una saturazione dei valori se superano i valori massimi consentiti
def scalatura_out(wdx,wsx,angle):

    angle=math.degrees(angle)

    #saturazione dei comandi:
    if angle > const.ANGLE_MAX:
        angle = const.ANGLE_MAX
    elif angle < -const.ANGLE_MAX:
        angle = -const.ANGLE_MAX

    if wdx > const.w_max:
        wdx = const.w_max
    elif wdx < -const.w_max:
        wdx = -const.w_max

    if wsx > const.w_max:
        wsx = const.w_max
    elif wsx < -const.w_max:
        wsx = -const.w_max

    # scalatura
    wdx=wdx/const.w_max # da -w_max/w_max a -1/1
    wdx=int(wdx*1023) # da -1/1 a -1023/1023

    wsx=wsx/const.w_max # da -w_max/w_max a 0/1
    wsx=int(wsx*1023) # da -1/1 a -1023/1023

    return wdx, wsx, angle


"""Funzioni per il calcolo delle variabili d'interesse"""

# calcola i valori di velocità lineare e angolare del modulo successivo a partire dagli stessi valori del modulo precedente
def kinematic(lin_vel_in,ang_vel_in,module,segno):
    global theta

    if segno==1:
        module=module+1
    theta_dot = -(1/const.b)*(ang_vel_in*(const.b+const.a*math.cos(theta[module]))+lin_vel_in*math.sin(theta[module]))
    #print('theta_dot: '+str(theta_dot)) #check
    theta[module]=theta[module]+theta_dot*const.Ts

    ang_vel_out = ang_vel_in + theta_dot

    lin_vel_out_x = lin_vel_in + const.b*math.sin(theta[module])*ang_vel_out
    lin_vel_out_y = -ang_vel_in*const.a - const.b*math.cos(theta[module])*ang_vel_out

    lin_vel_out = math.sqrt(lin_vel_out_x**2 + lin_vel_out_y**2)

    '''
    # pubblica sul topic "/tf" la posizione e l'orientamento del sistema di riferimento del secondo modulo denominato "RFM_2"
    # rispetto al sistema di riferimento fisso chiamato "RFM_1"
    # Si può visualizzare graficamente tramite rviz
    if module == 1:
        posa_M12=tf.TransformBroadcaster()
        x2=-const.a-const.b*math.cos(theta[module])
        y2=-const.b*math.sin(theta[module])
        posa_M12.sendTransform((x2,y2,0),
        tf.transformations.quaternion_from_euler(0, 0, theta[module]),
        rospy.Time.now(),
        "RFM_2",
        "RFM_1")
    if module == 2:
        posa_M23=tf.TransformBroadcaster()
        x3=-const.a-const.b*math.cos(theta[module])
        y3=-const.b*math.sin(theta[module])
        posa_M23.sendTransform((x3,y3,0),
        tf.transformations.quaternion_from_euler(0, 0, theta[module]),
        rospy.Time.now(),
        "RFM_3",
        "RFM_2")
        '''

    return lin_vel_out, ang_vel_out


# calcola wdx,wsx,wi in funzione della velocità lineare e angolare del modulo
def vel_motors(lin_vel,ang_vel,module):
    global theta

    wdx = (lin_vel+ang_vel*const.d/2)/const.r
    wsx = (lin_vel-ang_vel*const.d/2)/const.r

    angle = theta[module]

    return wdx, wsx, angle


"""Struttura ROS"""

# Elabora e pubblica le velocità di rotazione dei motori di avanzamento (wdx,wsx) e imbardata (wi) di ogni modulo.
# La funzione viene richiamata come callback della funzione listener non appena sono disponibili dei nuovi dati sul topic "remote_control"
def assegnazione_velocità(vel,curv):
    #print('\n\ndati ricevuti: vel:'+str(vel)+' curv:'+str(curv)) #check1

    # scalatura in ingresso
    lin_vel,curv = scalatura_in(vel,curv)
    #print('scalatura_in: vel:'+str(lin_vel)+' curv:'+str(curv)) #check2

    segno,lin_vel,curv = direzione_in(lin_vel,curv)
    #print('direzione_in: vel:'+str(lin_vel)+' curv:'+str(curv)+' segno:'+str(segno)) #check3

    # per ogni modulo ...
    if segno==1:
        vettore_moduli= list(range(const.N_MOD)) # in avanti
    else:
        vettore_moduli= list(range(const.N_MOD)) # indietro
        vettore_moduli.reverse()
    #print('vettore moduli: '+str(vettore_moduli)) #check4

    # da curvatura a velocità angolare
    ang_vel=curv2ang(lin_vel,curv)
    #print('curv2ang: ang_vel: '+str(ang_vel)) #check5

    # definizione variabili strutturate per ROS
    pub=rospy.Publisher("motor_topic",Motor,queue_size=10)
    motor_msg=Motor() #Motor.msg={wdx,wsx,angle}

    #print('CICLO FOR:') #check6
    # per ogni modulo ...
    for num_module in vettore_moduli:
        #print('modulo: '+str(num_module)) #check7

        wdx, wsx, angle = vel_motors(lin_vel,ang_vel,num_module) # ... calcola wdx,wsx,wi in funzione della velocità lineare e angolare del modulo
        #print('vel_motors: wdx: '+str(wdx)+' wsx: '+str(wsx)+' angle: '+str(angle)) #check8

        wdx, wsx, angle = direzione_out(wdx, wsx, angle, segno)
        #print('direzione_out: wdx:'+str(wdx)+' wsx:'+str(wsx)+' angle:'+str(angle)) #check9

        wdx, wsx, angle = scalatura_out(wdx,wsx,angle) # ... scala i valori in uscita
        #print('scalatura_out: wdx: '+str(wdx)+' wsx: '+str(wsx)+' angle: '+str(angle)) #check10

        print('modulo '+str(num_module)+' -> wsx:'+str(wsx)+' wdx'+str(wdx)+' angle:'+str(angle))

        motor_msg.wdx = wdx
        motor_msg.wsx = wsx
        motor_msg.angle = angle
        motor_msg.address = const.ADDRESSES[num_module]
        pub.publish(motor_msg) # ... tramette i valori wdx,wsx,angle sul topic "motor_topic"

        if num_module != vettore_moduli[-1]: # per tutti i moduli tranne l'ultimo ...
            lin_vel,ang_vel = kinematic(lin_vel,ang_vel,num_module,segno) # ... calcola i valori di velocità lineare e angolare del modulo successivo a partire dagli stessi valori del modulo precedente
            #print('kinematic modulo successivo: lin_vel: '+str(lin_vel)+' ang_vel: '+str(ang_vel)) #check11
    print('\n\n')

def vel_list(dataa):
    global vel
    vel=int(dataa.data)

def curv_list(dataa):
    global curv
    curv=int(dataa.data)
    assegnazione_velocità(vel,curv)

if __name__ == '__main__':
    try:
        rospy.init_node('agevar') #inizializza il nodo "agevar"
        rospy.loginfo("Hello! agevar node started!")

        rospy.Subscriber("vel",UInt16,vel_list)
        rospy.Subscriber("curv",UInt16,curv_list)

        rospy.spin()
        
    except rospy.ROSInterruptException:
        pass

# TODO: aggiungere equazioni nuove
# TODO: test funzionamento
