from agevar_constant import *
from math import cos, sin, sqrt

# compute the linear velocity and angular velocity of the next module
# from the values of the kinematic variables of the previous module

def moduleYawRateCorrection(delta,delta_meas):
    # Module yaw rate correction: corrects module's yaw rate (angular velocity around z, omega) taking in consideration the difference between computed and measured joint yaw angle
    ddelta = delta_meas - delta
    domega = ddelta/Ts
    return domega

def agevar_kinematic(lin_vel_in,ang_vel_in,delta,delta_meas,module,sign):
    if sign==1: # forward
        module=module+1
    else:       # backward
        module=module-1

    delta_dot = -(1/b)*(ang_vel_in*(b+a*cos(delta[module]))+lin_vel_in*sin(delta[module]))
    delta[module]=delta[module]+delta_dot*Ts

    ang_vel_out = ang_vel_in + delta_dot # theoretical module yaw rate (Omega, rotation around z)
    domega = moduleYawRateCorrection(delta,delta_meas)
    omega_corr = ang_vel_out + domega
    lin_vel_out_x = lin_vel_in + b*sin(delta[module])*omega_corr
    lin_vel_out_y = -ang_vel_in*a - b*cos(delta[module])*omega_corr



    lin_vel_out = sqrt(lin_vel_out_x**2 + lin_vel_out_y**2)

    return lin_vel_out, omega_corr