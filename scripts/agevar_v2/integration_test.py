import constant as const
import time
import numpy as np
import matplotlib.pyplot as plt

def calcola_posizione(ang_vel,index):
    global Ts_joystick
    global position_list
    new_pos = position_list[index]+ang_vel*Ts_joystick
    position_list.append(new_pos)



file = open("C:\\Users\\richi\Documents\GitHub\ReseQROS\scripts\\agevar_v2\\velocità_angolari.txt","r")
Ts_joystick = 1/const.JOYSTICK_FREQ

position_list = [0]
ang_vel_list = [0]
index = 0

for ang_value in file:
    time.sleep(Ts_joystick) #Questo serve a simulare la recezione di dati dal joystick con una certa frequenza
    calcola_posizione(float(ang_value),index)
    ang_vel_list.append(ang_value)
    index+=1

file.close()
# Dopo aver calcolato i valori delle posizione e aver salvato tutti i valori delle velocità angolari provo a plottarli
# per verificarne il funzionamento

if (len(position_list)!=len(ang_vel_list)):
    print("Errore, la dimensione dei due vettori non è la stessa")

#x = np.linspace(0,len(position_list),Ts_joystick)
plt.plot(position_list)
plt.plot(ang_vel_list)
plt.title("Plot della velocità angolare e relativa posizione")
plt.legend(['Posizione (phi)', 'Velocità angolare (phi_dot)'])
plt.show()

