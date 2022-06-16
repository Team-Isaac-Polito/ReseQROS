from math import cos, sin, radians, pi

# CONSTANTS

N_MOD = 2           # Number of modules of the robot

#serve ancora? TODO
N_VAR = 7           # Number of kinetic variables 

ANGLE_MAX = 35      # [°] Is the maximum angle between two moduless

FREQ = 50          # [Hz] Is the refresh rate of the program. Is you to determinate the time passed from the previous operation
Ts = 1/FREQ        # [s] Periodo di iterazione dell'algoritmo, da scegliere e implementare con ROS

ADDRESSES = [ 21, 48, 69 ] # 0x15, 0x30, 0x45

a = 0.15        # [m] distanza tra il punto centrale del modulo i-esimo e il giunto d'imbardata precedente

b = 0.15        # [m] distanza tra il punto centrale del modulo i-esimo e il giunto d'imbardata successivo

d = 0.1         # [m] lunghezza dell'interasse tra le due ruote equivalenti

r = 0.05        # [m] raggio delle ruote equivalenti

w_max = 5 # [Hz] massima velocità di rotazione di un motore di avanzamento

Max_Lin_Vel= w_max*r/2 # [m/s] massima velocità lineare di un modulo

Min_Curv = d/2 # [m] 
Max_Curv = 10*Min_Curv# [m]