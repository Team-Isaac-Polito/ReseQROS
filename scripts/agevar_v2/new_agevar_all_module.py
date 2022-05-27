import constant as const
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import time
import math

'''
Input: phid1, v1

Output:
phi1 -> integrale discreto di phid1
xd1 = cos(phi1) * v1
yd1 = sin(phi1) * v1
x1 -> integrale discreto di xd1
y1 -> integrale discreto di yd1


@Riccardo Giacchino [301168] e @Marco Barbon []
'''


Ts_joystick = 1/const.JOYSTICK_FREQ #la frequenza scelta è del tutto casuale, non è quella vera

def integrale_discreto(x,dx,index): # Funzione che esegue l'integrale discreto secondo la formula: x(k+1) = x(k) + dx(k)*Ts
    global Ts_joystick
    new_value = x[index]+dx*Ts_joystick
    x.append(new_value)

def velocità_lineari(phi1_i, v1_i):
    xd1 = math.cos(phi1_i)*v1_i
    yd1 = math.sin(phi1_i)*v1_i
    return xd1, yd1

def lettura_da_file(file_name):
    with open(file_name, 'r') as data:
        x = []
        y = []
        for line in data:
            p = line.split()
            x.append(float(p[0]))
            y.append(float(p[1]))

        data.close()

    return x, y

def model(y,t,xd_i_1,yd_i_1,phi_i_1,phid_i_1):
    dydt = ((yd_i_1*math.cos(y))-(xd_i_1*math.sin(y))-(const.a*math.cos(phi_i_1)*phid_i_1)*(math.cos(y)+math.sin(y)))/const.b
    return dydt

def agevar_module_1():
    # Lettura da file
    ang_vel, lin_vel = lettura_da_file('dati_in_input.dat') # Lettura dei dati da un file per simula la ricezione di valori 
                                                            # in input

    # Liste
    phi_1 = []  # Lista in cui vengono memorizzati tutti i valori di phi_1, in questo caso serve solo per il plot, come
                # per le altre liste, può essere sostituita da una semplice variabile per memorizzare solo il valore al
                # tempo k e calcolare quello al tempo k+1
    x1 = []
    y1 = []
    general_index = 0
    y0 = 0
    t = np.linspace(0,20)

    for phid1_i, v1_i in ang_vel, lin_vel: #questo loop è temporaneo, verrà sostituito con la lettura dei dati dal telecomando

        time.sleep(Ts_joystick) # Per simulare la lettura di dati con una certa frequenza

        # Modulo 1
        integrale_discreto(phi_1, phid1_i, general_index)   # Calcolo di phi1_i
        xd1, yd1 = velocità_lineari(phi_1[general_index], v1_i)
        integrale_discreto(x1, xd1, general_index)  # Calcolo di x1
        integrale_discreto(y1, yd1, general_index)  # Calcolo di y1

        # Modulo i-esimo
        phi_2 = odeint(model,y0,t,args=(xd1,yd1,phi_1(general_index),phid1_i))
        

        general_index+=1
        y0 = phi_2
    