import constant as const
import time
import numpy as np
import matplotlib.pyplot as plt

# Questo codice esegue il calcolo della posizione attraverso la computazione dell'integrale discreto
# x(k+1) = x(k) + dx(k)*Ts
# dove x(k+1) corrisponde al valore della posizione al tempo k+1, x(k) il valore della posizione al tempo attuale k, e 
# dx(k) è la derivata della posizione, quindi la velocità (nel nostro caso velocità angolare) che è passato come input
# Ts è il periodo che intercorre tra la ricezione di un valore dal joystick riferito alla velocità angolare

def calcola_posizione(ang_vel,index):
    global Ts_joystick
    global position_list
    new_pos = position_list[index]+ang_vel*Ts_joystick
    position_list.append(new_pos)


file = open("C:\\Users\\richi\Documents\GitHub\ReseQROS\scripts\\agevar_v2\\velocità_angolari.txt","r")
Ts_joystick = 1/const.JOYSTICK_FREQ #la frequenza scelta è del tutto casuale, non è quella vera

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

#Plot dei risultati
"""
plt.plot(position_list)
plt.plot(ang_vel_list)
plt.title("Plot della velocità angolare e relativa posizione")
plt.legend(['Posizione (phi)', 'Velocità angolare (phi_dot)'])
plt.xlabel()
plt.show()
"""

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(position_list, 'g-')
ax2.plot(ang_vel_list, 'b-')
ax1.set_xlabel('Iterazioni')
ax2.set_ylabel('Posizione angolare [rad]', color='g')
ax1.set_ylabel('Velocità angolare [rad/s]', color='b')
plt.title("Plot della velocità angolare e relativa posizione")
plt.show()

