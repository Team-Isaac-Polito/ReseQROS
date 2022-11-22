from agevar_constant import *

"""subfunctions of agevar_in"""

# Filters the vibration around the resting position
def filter(lin_vel,r_curv):
    lin_vel = 512 if 462 < lin_vel < 562 else lin_vel
    r_curv = 512 if 462 < r_curv < 562 else r_curv
    return lin_vel, r_curv

# Scales the inputs from topic "lin_vel and r_curv" from 0/1023 to their real values
def in_scaling(lin_vel,r_curv):
    # lin_vel:
    lin_vel = -(lin_vel-512) # from 0/1023 to 512/-511
    lin_vel = (lin_vel/512)*lin_vel_max # from -512/511 to -lin_vel_max/lin_vel_max

    # r_curv:
    r_curv = -(r_curv-512) # from 0/1023 to 512/-512
    if r_curv >= 0:
        r_curv = r_curv_max-(r_curv_max-r_curv_min)*r_curv/512 # from 0/511 to r_curv_max/r_curv_min
    else:
        r_curv = -r_curv_max-(r_curv_max-r_curv_min)*r_curv/512 # from -512/-1 to -r_curv_min/-r_curv_max
    return lin_vel, r_curv

# Computes the direction of the motion (forward or backward)
# and deals with backward motion's problems
def direction(lin_vel,r_curv):
    if (lin_vel<0):
        # backward:
        # sign=0 for convention
        # we invert the sign of lin_vel and r_curv, in order to treat this case as a forward movement,
        # indeed to do this we think the robot as it was in the reverse configuration (where the last module is the first and the first one is the last).
        # thus lin_vel becomes positive and r_curv change direction
        return 0, -lin_vel, -r_curv
    else:
        # forward:
        # sign=1
        # we leave unchanged the sign of lin_vel and r_curv
        return 1, lin_vel, r_curv

# It computes the angular velocity from the radius of curvature
def r_curv2ang(lin_vel,r_curv):
    ang_vel=lin_vel/r_curv

    if r_curv == r_curv_max or r_curv == -r_curv_max: #if the radius of curvature achieve his maximum value then the robot has to proceed forward without steering
        ang_vel=0

    return ang_vel


"""main function of agevar_in"""

def agevar_in(lin_vel,r_curv):
    lin_vel,r_curv=filter(lin_vel,r_curv)
    lin_vel,r_curv = in_scaling(lin_vel,r_curv)
    sign,lin_vel,r_curv = direction(lin_vel,r_curv)
    ang_vel=r_curv2ang(lin_vel,r_curv)

    return sign,lin_vel,ang_vel