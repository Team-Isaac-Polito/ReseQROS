from agevar_constant import *
from math import cos, sin

# compute the linear velocity and angular velocity of the next module
# from the values of the kinematic variables of the previous module
def agevar_kinematic(lin_vel_in,ang_vel_in,delta,module,sign):
    if sign==1: # forward
        module=module+1
    else:       # backward
        module=module-1

    lin_vel_out = lin_vel_in +a*ang_vel_in*sin(delta)
    ang_vel_out = (lin_vel_in*sin(delta)-a*ang_vel_in*cos(delta))/b

    return lin_vel_out, ang_vel_out