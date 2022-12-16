from math import pi

# GEOMETRIC CONSTANTS
N_mod = 3       # [-] Number of modules of the robot
a = 0.18        # [m] Distance between the center of every module and the previous yaw joint
b = 0.18        # [m] Distance between the center of every module and the following yaw joint
d = 0.21        # [m] Distance between pair of equivalent wheels
r_eq = 0.05     # [m] Radius of the equivalent wheels
delta_max = 35  # [°] Maximum delta (relative angle between two modules) achievable

# PERFORMANCE CONSTANTS
w_max = 2*pi                    # [rad/s] maximum rotation speed of the equivalent wheel (feed motor)
lin_vel_max = (w_max*r_eq)/2    # [m/s]   maximum linear speed of every module (half of the maximum achievable linear speed in order to make feasible the turns)
r_curv_min = 3*d                # [m]     minimum radius of curvature
r_curv_max = 10*r_curv_min      # [m]     maximum radius of curvature

# DATA TRANSMISSION
freq = 50        # [Hz] Transmission rate of the remote controller
Ts = 1/freq      # [s] Sampling time of the data acquired from the remote controller
address = [ 21, 22, 23 ] # 0x15, 0x16, 0x17

# PLOT PARAMETERS
t_sim=60
N_plot=20
envelope=True