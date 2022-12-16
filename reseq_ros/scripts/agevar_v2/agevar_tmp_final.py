from glob import glob
from operator import ne
import constant as const
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import time
import math
import rospy
from ReseQROS.msg import Remote, Motor


Ts = 10 # Frequenza di iterazione dell'algoritmo, da scegliere e implementare con ROS

kin_vars = np.zeros((const.N_MOD, const.N_VAR))  # Matrice che contiene tutte le variabili cinematiche di tutti i moduli
                                                # necessarie per il calcolo delle velocità. Dimensionata come numero di 
                                                # moduli * numero di variabili usata (attualmente 7)
                                                # Riga generica: [phid_i, phi_i, xd_i, x_i, yd_i, y_i, v_i]

# CALLBACK per la funzione di lettura da joystick (Marco)
# 
#
# 

"""Funzioni generali"""

def calcolo_integrale_discreto(num_module, var):

    # Dato il numero del modulo e il tipo di variabile cinematica (che può essere la velocità angolare phid o quella
    # lineare) calcolo il suo integrale discreto come x(k+1) = x(k) + dx(k)*Ts, dove Ts è il tempo trascorso
    # dall'iterazione precedente, imposto da noi tramite funzione sleep di ROS

    global Ts
    global kin_vars
    dx_i = kin_vars[num_module][var]
    x_i = kin_vars[num_module][var+1]
    new_value = x_i+dx_i*Ts
    kin_vars[num_module][var] = new_value
    #return new_value

def calcolo_velocità_lineare_modulo_1():

    # Funzione che calcola le velocità lineari solo del modulo 1 (in quanto ha funzioni diverse rispetto agli altri moduli)

    global kin_vars
    phi1 = kin_vars[0][1]
    v1 = kin_vars[0][6]
    xd1 = math.cos(phi1)*v1
    yd1 = math.sin(phi1)*v1
    kin_vars[0][2] = xd1
    kin_vars[0][4] = yd1
    #return xd1, yd1

def lettura_da_file(file_name): #Temporanea lettura da file
    with open(file_name, 'r') as data:
        x = []
        y = []
        for line in data:
            p = line.split()
            x.append(float(p[0]))
            y.append(float(p[1]))

        data.close()

    return x, y

def velocità_motori(ang_vel,lin_vel):
    wdx = (lin_vel[-1]+ang_vel[-1]*const.d/2)/const.r
    wsx = (lin_vel[-1]-ang_vel[-1]*const.d/2)/const.r
    wi = 0
    return wdx, wsx, wi

def agevar_module_1(ang_vel, lin_vel):

    global kin_vars

    kin_vars[0][0] = ang_vel
    kin_vars[0][0] = lin_vel

    calcolo_integrale_discreto(0,0)   # Calcolo di phi1
    calcolo_velocità_lineare_modulo_1() # Calcolo xd1 e yd1
    calcolo_integrale_discreto(0,2)  # Calcolo di x1
    calcolo_integrale_discreto(0,4)  # Calcolo di y1
    
    #rospy.loginfo("phi1: %f, phid1: %f, x1: %f, y1: %f, xd1: %f, yd1: %f, v1: %f" % (phi1[-1], phid1[-1], x1[-1], y1[-1], xd1[-1], yd1[-1], v1[-1]))
    #TODO da togliere rospy.loginfo

    wdx, wsx, wi = velocità_motori(kin_vars[0][0], kin_vars[0][6])

    return wdx, wsx, wi

def model_1(y,t,num_module):
    
    global kin_vars
    xd_i_1 = kin_vars[num_module-1][2]
    yd_i_1 = kin_vars[num_module-1][4]
    phi_i_1 = kin_vars[num_module-1][1]
    phid_i_1 = kin_vars[num_module-1][0]
    dydt = ((yd_i_1*math.cos(y))-(xd_i_1*math.sin(y))-(const.a*math.cos(phi_i_1)*phid_i_1)*(math.cos(y)+math.sin(y)))/const.b
    return dydt

def agevar_module_i():
