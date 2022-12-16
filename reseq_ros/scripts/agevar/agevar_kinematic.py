from agevar_constant import *
from math import cos, sin, sqrt

# compute the linear velocity and angular velocity of the next module
# from the values of the kinematic variables of the previous module
def agevar_kinematic(lin_vel_in,ang_vel_in,delta,module,sign):
    if sign==1: # forward
        module=module+1
    else:       # backward
        module=module-1

    delta_dot = -(1/b)*(ang_vel_in*(b+a*cos(delta[module]))+lin_vel_in*sin(delta[module]))
    delta[module]=delta[module]+delta_dot*Ts

    ang_vel_out = ang_vel_in + delta_dot

    lin_vel_out_x = lin_vel_in + b*sin(delta[module])*ang_vel_out
    lin_vel_out_y = -ang_vel_in*a - b*cos(delta[module])*ang_vel_out



    lin_vel_out = sqrt(lin_vel_out_x**2 + lin_vel_out_y**2)

    return lin_vel_out, ang_vel_out