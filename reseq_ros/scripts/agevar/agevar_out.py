from agevar_constant import *
from math import degrees

"""subfunctions of agevar_out"""

# Takes into account the saturation of the commands
def saturation(wdx,wsx,angle):
    angle=degrees(angle)

    if angle > delta_max:
        angle = delta_max
    elif angle < -delta_max:
        angle = -delta_max

    if wdx > w_max:
        wdx = w_max
    elif wdx < -w_max:
        wdx = -w_max

    if wsx > w_max:
        wsx = w_max
    elif wsx < -w_max:
        wsx = -w_max

    return wdx, wsx, angle

# Scales the output values used to feed the topic "motor_topic" from the real values to 0/1023
def out_scaling(wdx,wsx):
    wdx=wdx/w_max # from -w_max/w_max to -1/1
    wdx=int(wdx*1023) # from -1/1 to -1023/1023

    wsx=wsx/w_max # from -w_max/w_max to 0/1
    wsx=int(wsx*1023) # from -1/1 to -1023/1023

    return wdx, wsx

# It computes wdx,wsx,angle from the linear and angular velocity of the module
def vel_motors(lin_vel,ang_vel,delta,num_module):
    wdx = (lin_vel+ang_vel*d/2)/r_eq
    wsx = (lin_vel-ang_vel*d/2)/r_eq
    angle = delta[num_module]

    return wdx, wsx, angle

"""main function of agevar_out"""

def agevar_out(num_module,sign,lin_vel,ang_vel,delta):
    wdx, wsx, angle = vel_motors(lin_vel,ang_vel,delta,num_module)
    wdx, wsx, angle = saturation(wdx,wsx,angle)
    wdx, wsx = out_scaling(wdx,wsx)

    if sign == 0:  # backward
        wsx, wdx = -wsx,-wdx

    return wdx, wsx, angle