#!/usr/bin/env python

import rospy
import constant as const

#prova di commit

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
        nomi_file[i] = const.FILE_PATH+str(i)+".txt"
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

# Si occupano della scrittura dei valori su file, necessario per la memorizzazione e lettura dei valori precedenti
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
    invio_token(vdx, vsx, angle, 0) # TODO: aggiungere oltre a questa riga di codice, il codice necessario per inviare al token
                                    # i valori di riferimento del primo modulo

    # Controllo se la velocità arrivata come input è nulla, indipendentemente dal valore della curvatura (nel caso in cui
    # si fermasse in curva).
    if (vel == 0):
        for i in range(1,const.N_MOD):
            # TODO: Inserire codice per inviare token per ogni modulo successivo al primo
            print("%f %f %f\n" %(vdx,vsx,angle))
        return None # Termina l'iterazione per proseguire alla successiva.

    # Ritardo
    # Caloclo del ritardo basato sulla velocità con cui sta iniziando la curva.
    if (curv != 0.5 and trigger == 1):
        trigger = 0
        for i in range(1,const.N_MOD):
            ritardo[i] = i*const.DIST_MOD/vel

    # Assegnazione ai rimanenti moduli
    for i in range(1,const.N_MOD):  # Per ogni modulo successivo al primo ricalcolo il ritardo e determino inviare
                                    # al token in base alle diverse condizioni.
        if(ritardo[i] > 0): # In questo caso devo ancora attendere che si esaurisca il ritardo, quindi mantengo la stessa
                            # velocità dell'iterazione precedente.
            ritardo[i] -= 1/const.FREQ  # Al ritardo viene tolto un tempo corrispondente al tempo trascorso dalla scorsa
                                        # iterazione. Dato che il refresh rate è di 50 Hz, il tempo trascorso è 1/50.
            with open(nomi_file[i], 'r') as f:  # Leggo da file i valori e li invio al token.
                data = f.read()
                f.close()
                data = data.split()
                vdx_2 = float(data[0])
                vsx_2 = float(data[1])
                angle_2 = float(data[2])
                invio_token_v2(vdx_2, vsx_2, angle_2, i)    # TODO: questa riga va sostituita con il codice per inviare
                                                            # i valori al token.
        else:
            # Siamo nella condizione in cui il ritardo del modulo i-esimo è pari a 0, quindi ogni modulo legge
            # i valori di riferimento dal file del primo modulo, aggiornado il puntatore del file alla riga successiva
            # dopo aver eseguito l'istruzione di lettura.

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
                # TODO: In questo caso la riga di codice 'invio_token_v2' non va sostituita, in quanto necessaria
                # per memorizzare nel file i valori di riferimento, che verranno letti nel caso in cui il ritardo del
                # modulo fosse maggiore di 0
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
