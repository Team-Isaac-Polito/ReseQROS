#!/usr/bin/env python3

import rospy
from ReseQROS.msg import Remote, Motor
import tf
import constant as const
import math
import numpy as np

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

Ts = 1/const.FREQ # Frequenza di iterazione dell'algoritmo, da scegliere e implementare con ROS

kin_vars = np.zeros((const.N_MOD, const.N_VAR))  # Matrice che contiene tutte le variabili cinematiche di tutti i moduli
                                                # necessarie per il calcolo delle velocità. Dimensionata come numero di 
                                                # moduli * numero di variabili usata (attualmente 7)
                                                # Riga generica: [phid_i, phi_i, xd_i, x_i, yd_i, y_i, v_i]

"""Funzioni generali"""

def calcolo_integrale_discreto(num_module, var):
    #num_module: 0->(const.N-1)
    #var: phid_i=0, xd_i=2, yd_i=4

    # Dato il numero del modulo e il tipo di variabile cinematica (che può essere la velocità angolare phid o quella
    # lineare) calcolo il suo integrale discreto come x(k+1) = x(k) + dx(k)*Ts, dove Ts è il tempo trascorso
    # dall'iterazione precedente, imposto da noi tramite funzione sleep di ROS

    global Ts
    global kin_vars
    dx_i = kin_vars[num_module][var]
    x_i = kin_vars[num_module][var+1]
    new_value = x_i+dx_i*Ts
    kin_vars[num_module][var+1]= new_value
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

def velocità_motori(num_module):
    global kin_vars

    # wdx,wsx:
    ang_vel=kin_vars[num_module][0]
    lin_vel=kin_vars[num_module][6]

    wdx = (lin_vel+ang_vel*const.d/2)/const.r
    wsx = (lin_vel-ang_vel*const.d/2)/const.r

    # wi:
    # 2-> modulo i
    # 1-> modulo i-1
    ang_vel_2=kin_vars[num_module][0]
    ang_vel_1=kin_vars[num_module-1][0]

    if num_module==0:
        wi = 0
    else:
        wi= ang_vel_1-ang_vel_2 #TODO da controllare il segno (non ne sono sicuro...)
    
    return wdx, wsx, wi

def agevar_module_1(ang_vel, lin_vel):
    global kin_vars

    kin_vars[0][0] = ang_vel
    kin_vars[0][6] = lin_vel

    calcolo_integrale_discreto(0,0)   # Calcolo di phi1
    calcolo_velocità_lineare_modulo_1() # Calcolo xd1 e yd1
    calcolo_integrale_discreto(0,2)  # Calcolo di x1
    calcolo_integrale_discreto(0,4)  # Calcolo di y1
    
    # pubblica sul topic "/tf" la posizione e l'orientamento del sistema di riferimento del primo modulo denominato "RFM_1"
    # rispetto al sistema di riferimento fisso chiamato "map"
    # Si può visualizzare graficamente tramite rviz
    posa_M1=tf.TransformBroadcaster()
    posa_M1.sendTransform((kin_vars[0][3],kin_vars[0][5],0),
    tf.transformations.quaternion_from_euler(0, 0, kin_vars[0][1]),
    rospy.Time.now(),
    "RFM_1",
    "map")

    wdx, wsx, wi = velocità_motori(0)

    return wdx, wsx, wi

# def agevar_module_i(num_module):
#     global kin_vars

#     # 2-> modulo i
#     # 1-> modulo i-1
#     phid_1=kin_vars[num_module-1][0]
#     phi_1=kin_vars[num_module-1][1]
#     xd_1=kin_vars[num_module-1][2]
#     yd_1=kin_vars[num_module-1][4]

#     phi_2=kin_vars[num_module][1]

#     print(phid_1,phi_1,xd_1,yd_1,phi_2) #TODO da cancellare
    
#     # Calcolo di phid_2
#     phid_2=(-xd_1*math.sin(phi_2)+yd_1*math.cos(phi_2)-(const.a*math.cos(phi_1)*phid_1)*(math.sin(phi_2)+math.cos(phi_2)))/const.b
#     kin_vars[num_module][0]=phid_2

#     print(phid_2)

#     # Calcolo di phi_2
#     calcolo_integrale_discreto(num_module,0)   
    
#     # Calcolo di xd_2
#     xd_2=xd_1+const.b*math.sin(phi_2)*phid_2+const.a*math.sin(phi_1)*phid_1
#     kin_vars[num_module][2]=xd_2

#     #Calcolo di x_2

#     calcolo_integrale_discreto(num_module,2) 

#     # Calcolo di yd_2
#     yd_2=yd_1-const.b*math.cos(phi_2)*phid_2+const.a*math.cos(phi_1)*phid_1
#     kin_vars[num_module][4]=yd_2

#     #Calcolo di y_2
#     calcolo_integrale_discreto(num_module,4) 

#     # pubblica sul topic "/tf" la posizione e l'orientamento del sistema di riferimento del i-esimo modulo denominato "RFM_i"
#     # rispetto al sistema di riferimento fisso chiamato "map"
#     # Si può visualizzare graficamente tramite rviz
#     posa_M_i=tf.TransformBroadcaster()
#     posa_M_i.sendTransform((kin_vars[num_module][3],kin_vars[num_module][5],0),
#     tf.transformations.quaternion_from_euler(0, 0, kin_vars[num_module][1]),
#     rospy.Time.now(),
#     "RFM_"+str(num_module+1),
#     "map")

#     #TODO calcolare v_i

#     wdx, wsx, wi = velocità_motori(num_module)

#     return wdx, wsx, wi

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
    for num_module in range(const.N_MOD):
        if num_module==0:
            wdx, wsx, wi = agevar_module_1(ang_vel,lin_vel) # Modulo 1
        else:
            wdx, wsx, wi = agevar_module_i(num_module) # Modulo i-esimo
        
        motor_msg.wdx = int(wdx) #TODO float o int?
        motor_msg.wsx = int(wsx) #TODO float o int?
        motor_msg.wi = int(wi)   #TODO float o int?
        motor_msg.address = const.ADDRESSES[num_module]

        pub.publish(motor_msg)

# legge i comandi di alto livello dal topic "remote_topic" e
# applica la funzione assegnazione_velocità ai valori ricevuti
def listener():
    rospy.Subscriber("remote_topic",Remote,assegnazione_velocità)

def posizione_di_partenza():
    global kin_vars

    for num_module in range(1,const.N_MOD):
        kin_vars[num_module][3]=-1*(const.a+const.b)*num_module
    print(kin_vars)

def main_function():

    rospy.init_node('agevar') #inizializza il nodo "agevar"
    rospy.loginfo("Hello! agevar node started!")

    #listener()
    #rospy.spin()

    posizione_di_partenza()

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

# TODO: connettere il nodo ad un telecomando per testare il suo funzionamento
