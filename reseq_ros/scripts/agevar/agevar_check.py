from agevar_constant import *

import matplotlib.pyplot as plt
from math import cos, sin
import random
# import numpy as np

x0=[0]
y0=[0]
dx0=[0]
dy0=[0]
theta0=[0]

x1=[-a-b]
y1=[0]
dx1=[0]
dy1=[0]
theta1=[0]

x2=[-2*a-2*b]
y2=[0]
dx2=[0]
dy2=[0]
theta2=[0]

graph=1

def check_sim(num_module,lin_vel,ang_vel):
    global x0,dx0,y0,dy0,theta0,x1,dx1,y1,dy1,theta1,x2,dx2,y2,dy2,theta2,graph

    if num_module==0:
        x0.append(x0[-1]+lin_vel*cos(theta0[-1])*Ts)
        dx0.append(cos(theta0[-1]))
        y0.append(y0[-1]+lin_vel*sin(theta0[-1])*Ts)
        dy0.append(sin(theta0[-1]))
        theta0.append(theta0[-1]+ang_vel*Ts)
    
    if num_module==1:
        x1.append(x1[-1]+lin_vel*cos(theta1[-1])*Ts)
        dx1.append(cos(theta1[-1]))
        y1.append(y1[-1]+lin_vel*sin(theta1[-1])*Ts)
        dy1.append(sin(theta1[-1]))
        theta1.append(theta1[-1]+ang_vel*Ts)

    if num_module==2:
        x2.append(x2[-1]+lin_vel*cos(theta2[-1])*Ts)
        dx2.append(cos(theta2[-1]))
        y2.append(y2[-1]+lin_vel*sin(theta2[-1])*Ts)
        dy2.append(sin(theta2[-1]))
        theta2.append(theta2[-1]+ang_vel*Ts)

    if len(x2)==int(t_sim/Ts) and graph==1:
        fig, ax = plt.subplots()
        ax.set_aspect('equal','box')
        ax.set_adjustable("datalim")
        
        if envelope: # envelope of the curves
            plt.quiver(x0,y0,dx0,dy0,color='r')
            plt.quiver(x1,y1,dx1,dy1,color='b')
            plt.quiver(x2,y2,dx2,dy2,color='k')
            
        else: # N position over the overall time

            step=int(len(x2)/N_plot)

            for k in range(N_plot):
                r=random.random()
                g=random.random()
                b=random.random()
                color=[(r,g,b)]
                plt.quiver(x0[k*step],y0[k*step],dx0[k*step],dy0[k*step],color=color)
                plt.quiver(x1[k*step],y1[k*step],dx1[k*step],dy1[k*step],color=color)
                plt.quiver(x2[k*step],y2[k*step],dx2[k*step],dy2[k*step],color=color)

            '''
            i=int(t_sim/4/Ts)
            bound=50
            i=i-bound

            for k in range(i,i+2*bound,15):
                r=random.random()
                g=random.random()
                b=random.random()
                color=[(r,g,b)]
                plt.quiver(x0[k],y0[k],dx0[k],dy0[k],color=color)
                plt.quiver(x1[k],y1[k],dx1[k],dy1[k],color=color)
                plt.quiver(x2[k],y2[k],dx2[k],dy2[k],color=color)
            '''
            
        plt.show()
        graph=0

def check_print1(num_module,module_vector,lin_vel,ang_vel):
    print('num_mod: ',num_module,' ->      lin_vel: ',lin_vel,'      ang_vel: ',ang_vel)
    if num_module==module_vector[-1]:
        print('\n')

def check_print2(num_module,module_vector,wdx,wsx,angle):
    print('num_mod: ',num_module,' ->      angle: ',angle,'      wdx: ',wdx,'      wsx: ',wsx)
    if num_module==module_vector[-1]:
        print('\n')
