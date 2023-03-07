from math import pi

# GEOMETRIC CONSTANTS
N_mod = 3       # [-] Number of modules of the robot
a = 0.16        # [m] Distance between the center of every module and the previous yaw joint
b = 0.18        # [m] Distance between the center of every module and the following yaw joint
d = 0.21        # [m] Distance between pair of equivalent wheels
r_eq = 0.05     # [m] Radius of the equivalent wheels
delta_max = 35  # [°] Maximum delta (relative angle between two modules) achievable

# PERFORMANCE CONSTANTS
r_curv_min = 3*d                # [m]     minimum radius of curvature
r_curv_max = 10*r_curv_min      # [m]     maximum radius of curvature

rpm2rads = 2*pi/60
rads2rpm = 60/(2*pi)
sat = 5/7 # saturation security coefficient
w_max = 65*sat*rpm2rads           # [rad/s] maximum rotation speed of the equivalent wheel (feed motor)
w_c = w_max*r_curv_min/(r_curv_min+d/2)
lin_vel_max = w_c*r_eq          # [m/s]   maximum linear speed of every module

# DATA TRANSMISSION
freq = 50        # [Hz] Transmission rate of the remote controller
Ts = 1/freq      # [s] Sampling time of the data acquired from the remote controller
address = [ 21, 22, 23 ] # 0x15, 0x16, 0x17
