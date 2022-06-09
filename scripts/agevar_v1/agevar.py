#!/usr/bin/env python3

import rospy
import constant as const
from ReseQROS.msg import Remote, Motor
from std_msgs.msg import UInt16

#prova di commit

# Variabili globali
trigger = 1 #Dopo che è le velocità sono state ritardate per la prima volta, il ritardo viene mantenuto. Questo flag fa
			#in modo che non venga ricalcolato
ritardo = [0] * (const.N_MOD)	#Vettore dei ritardi. Ogni cella corrisponde al ritardo del modulo associato all'indice
puntatore_file = [0] * (const.N_MOD)
nomi_file = [None] * (const.N_MOD) 	#Nome dei file associati ad ogni modulo.

# Creazione e formattazione dei file sulla quale verranno salvati i dati dei diversi moduli.
# Un file per ogni modulo, il cui nome viene salvato di un array di stringhe. La cella dell'array corrisponde al modulo
def reset_file():
    global nomi_file
    for i in range(const.N_MOD):
        nomi_file[i] = const.FILE_PATH+str(i)+".txt"
        
        with open(nomi_file[i], 'w') as f:
            f.write("0 0 0\n")  #Inizializzazione dei file di salvataggio dati (inizializzazione necessaria in caso di ritardo>0 per richiamare i dati dai file)
            f.close()
            

# Dati in ingresso le coordinate del telecomando calcola i valori di riferimento usando le formule proposte
def calcolo_valori(velocita, curvatura):

    vsx = int(velocita + curvatura/2)
    vdx = int(velocita - curvatura/2)
    angle = int(curvatura/512*const.ANGLE_MAX)
    return vdx, vsx, angle

# Si occupano della scrittura dei valori su file, necessario per la memorizzazione e lettura dei valori precedenti
def invio_token(vdx, vsx, angle, index):
    global nomi_file
    with open(nomi_file[index], 'a') as f:
        f.write("%d %d %d\n" %(vdx,vsx,angle))
        f.close()
def invio_token_v2(vdx, vsx, angle, index):
    global nomi_file
    with open(nomi_file[index], 'w') as f:
        f.write("%d %d %d\n" %(vdx,vsx,angle))
        f.close()

def controllo_input(vel, curv):
    velo = 512 if 462 < vel < 562 else vel
    curvo = 512 if 462 < curv < 562 else curv
    vel = vel - 512
    curvo = curvo - 512
    return velo, curvo
	

#Funzione principale per il calcolo delle velocità di ogni modulo. Si occupa di ritardare le velocità dei moduli
#La funzione viene richiamata come callback della funzione listener non appena sono disponibili dei nuovi dati sul topic remote_control
def assegnazione_velocità(curv, args):
    global trigger
    global ritardo
    global puntatore_file
    global nomi_file

    #definizione variabili strutturate per ROS
    pub=rospy.Publisher("motor_topic",Motor,queue_size=10)
    motor_msg=Motor() #Motor.msg={vdx,vsx,angle}

    #dati letti sul topic remote_control
    vel = args[0]
    curv = curv

    vel, curv = controllo_input(vel, curv)


    #calcolo e log dei valori da passare al modulo di testa
    vdx, vsx, angle = calcolo_valori(vel, curv)   
    rospy.loginfo("vdx: %d, vsx: %d, angle: %d" % (vdx, vsx, angle))

    #salvataggio valori calcolati
    invio_token(vdx, vsx, angle, 0)
                                    
    #trasmissione dei valori calcolati per il modulo di testa come messaggio Motor() sul topic motor_topic_1
    motor_msg.vdx = vdx
    motor_msg.vsx = vsx
    motor_msg.angle = angle
    motor_msg.address = const.ADDRESSES[0]
    pub.publish(motor_msg)

    # Controllo se la velocità arrivata come input è nulla, indipendentemente dal valore della curvatura (nel caso in cui
    # si fermasse in curva).
    if (vel == 0):
        for i in range(1,const.N_MOD):
            # Nel caso di velocità nulla, anche tutti gli altri motori dovranno fermarsi, mantenedo comunqune l'angolo tra i moduli.
            # Questa operazione non viene salvata nel file, in modo tale da mantenere memorizzati i dati prima che il robot si fermasse, e rileggerli
            # non appena riprende il moto.
            motor_msg.vdx = vdx
            motor_msg.vsx = vsx
            motor_msg.angle = angle
            motor_msg.address = const.ADDRESSES[i]

            pub.publish(motor_msg)

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
                motor_msg.vdx = int(data[0])
                motor_msg.vsx = int(data[1])
                motor_msg.angle = int(data[2])
                motor_msg.address = const.ADDRESSES[i]

                pub.publish(motor_msg)
                
        else:
            # Siamo nella condizione in cui il ritardo del modulo i-esimo è pari a 0, quindi ogni modulo legge
            # i valori di riferimento dal file del primo modulo, aggiornado il puntatore del file alla riga successiva
            # dopo aver eseguito l'istruzione di lettura.

            with open(nomi_file[0], 'r') as f:
                f.seek(puntatore_file[i], 0)
                data = f.readline()
                puntatore_file[i] = f.tell()
                f.close()

                #salvataggio dati
                data = data.split()
                vdx_2 = int(data[0])
                vsx_2 = int(data[1])
                angle_2 = int(data[2])
                invio_token_v2(vdx_2, vsx_2, angle_2, i)

                #pubblicazione dati
                motor_msg.vdx = vdx_2
                motor_msg.vsx = vsx_2
                motor_msg.angle = angle_2
                motor_msg.address = const.ADDRESSES[i]

                pub.publish(motor_msg)

                ritardo[i] = 0

def ros_annidato(vel):
    rospy.Subscriber("curv",UInt16,assegnazione_velocità, (vel.data))

#legge i comandi di alto livello sul topic custom_chatter e
#applica la funzione assegnazione_velocità se sono disponibili dati sul topic custom_chatter
def listener():
    rospy.Subscriber("vel",UInt16,ros_annidato) # nome topic da cambiare

def main_function():
	reset_file()
	rospy.init_node('agevar')
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
