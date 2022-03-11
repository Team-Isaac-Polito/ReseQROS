#!/usr/bin/env python

import rospy
import constant as const

# Variabili globali
trigger = 1 #Dopo che è le velocità sono state ritardate per la prima volta, il ritardo viene mantenuto. Questo flag fa
			#in modo che non venga ricalcolato
ritardo = [0] * (const.N_MOD)	#Vettore dei ritardi. Ogni cella corrisponde al ritardo del modulo associato all'indice
puntatore_file = [0] * (const.N_MOD)
nomi_file = [None] * (const.N_MOD) 	#Nome dei file associati ad ogni modulo. Credo che non servirà più quanto sostituiremo la
									#scrittura sul file con la pubblicazione dei token


# Creazione e formattazione dei file sulla quale verranno salvati i dati dei diversi moduli.
# Un file per ogni modulo, il cui nome viene salvato di un array di stringhe. La cella dell'array corrisponde al modulo
def reset_file():
    global nomi_file
    for i in range(const.N_MOD):
        nomi_file[i] = "./Python_Course/Project_files_txt/coppie_"+str(i)+".txt"
        open(nomi_file[i], 'w').close()

# Fuzione per leggere i valori dal telecomando (attualmente li legge da tastiera) ed effettuata dei semplici controlli
def lettura_valori_da_telecomando():

    velocita = float(input("V [m/s]: "))
    curvatura = float(input("C (conpresa tra 0 e 1): "))

    #Controlli
    if(curvatura > 1 or curvatura < 0):
        print("Il valore della curvatura non è corretto")
        exit

    return velocita, curvatura

# Dati in ingresso le coordinate del telecomando calcola i valori di riferimento usando le formule proposte
def calcolo_valori(velocita, curvatura):

    vsx = velocita*(1-curvatura)
    vdx = velocita*curvatura
    angle = 2*(curvatura-0.5)*const.ANGLE_MAX

    return vdx, vsx, angle

# Due funzioni che ora scrivono su un file, ma andranno sostituite con le funzioni per inviare i token
def invio_token(vdx, vsx, angle, index):
    global nomi_file
    with open(nomi_file[index], 'a') as f:
        f.write("%f %f %f\n" %(vdx,vsx,angle))
        f.close()
def invio_token_v2(vdx, vsx, angle, index):
    global nomi_file
    with open(nomi_file[index], 'w') as f:
        f.write("%f %f %f\n" %(vdx,vsx,angle))
        f.close()

#Funzione principale per il calcolo delle velocità di ogni modulo. Si occupa di ritardare le velocità dei moduli
def assegnazione_velocità():
    global trigger
    global ritardo
    global puntatore_file
    global nomi_file

    vel, curv = lettura_valori_da_telecomando()
    vdx, vsx, angle = calcolo_valori(vel, curv)
    invio_token(vdx, vsx, angle, 0) #questi corrispondolo ai dati da inviare al primo modulo

    # Ritardo
    # Caloclo del ritardo basato sulla velocità con cui sta iniziando la curva
    if (curv != 0.5 and trigger == 1):
        trigger = 0
        for i in range(1,const.N_MOD):
            ritardo[i] = i*const.DIST_MOD/vel

    # Assegnazione ai rimanenti moduli
    for i in range(1,const.N_MOD): # Per ogni modulo successivo al primo eseguo calcolo e attuo il ritardo
        if(ritardo[i] > 0):
            ritardo[i] -= 1/const.FREQ  #Al ritardo viene tolto un tempo corrispondente al tempo trascorso dalla scorsa
                                        #operazione. Dato che il refresh rate è di 50 Hz, il tempo trascorso è 1/50
            with open(nomi_file[i], 'r') as f:
                data = f.read()
                f.close()
                data = data.split()
                vdx_2 = float(data[0])
                vsx_2 = float(data[1])
                angle_2 = float(data[2])
                invio_token_v2(vdx_2, vsx_2, angle_2, i)
        else:
            # Leggi dal file del primo module le velocità
            # memorizza la posizione del puntatore
            with open(nomi_file[0], 'r') as f:
                f.seek(puntatore_file[i], 0)
                data = f.readline()
                puntatore_file[i] = f.tell()
                f.close()
                data = data.split()
                vdx_2 = float(data[0])
                vsx_2 = float(data[1])
                angle_2 = float(data[2])
                invio_token_v2(vdx_2, vsx_2, angle_2, i)
                ritardo[i] = 0

def talker():
	reset_file()
	rospy.init_node('agevar')
	rate = rospy.Rate(50) #frecuency in hertz

	rospy.loginfo("Hello! agevar node started!")

	while not rospy.is_shutdown():
		rospy.loginfo("agevar node working")
		#ToDo
		# - check if something to read on topic
		assegnazione_velocità()
		# - publish output data on topic
		rate.sleep()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
