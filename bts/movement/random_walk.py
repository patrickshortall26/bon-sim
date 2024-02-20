import numpy as np
from math import atan, pi, cos, sin

def get_offset(x,y):
    quadrant_map = {(1,1) : 0, (1,-1) : pi/2, (-1,-1) : pi, (-1,1) : 3*pi/2}
    vel_signs = (np.sign(x), np.sign(y))
    offset = quadrant_map[vel_signs]
    return offset

def get_direction(vel):
    # Unpack
    x, y = vel[0], vel[1]
    # Calculate offset to add to direction
    offset = get_offset(x,y)
    # Calculate direction
    direction = atan(abs(y/x)) + offset
    return direction

def generate_random_number():
    rng = np.random.default_rng()
    random_number = rng.random()
    return random_number

def map(random_number):
    """
    Map random number in [0,1] to [0,2*pi]
    """
    return 2*pi*random_number

def generate_turning_amount():
    """
    Generate a turning amount randomly between 0 and 2pi
    """
    random_number = generate_random_number()
    turning_amount = map(random_number)
    return turning_amount

def turn(agent):
    if agent.time_straight == agent.time_before_turn:
        return True
    else:
        return False

def update_vel(agent):
    """
    Update 
    """
    old_vel = agent.vel
    if turn(agent):
        current_direction = get_direction(old_vel)
        turning_amount = generate_turning_amount()
        new_direction = current_direction + turning_amount
        magnitude = np.linalg.norm(agent.vel)
        new_vel = np.array([magnitude*sin(new_direction), magnitude*cos(new_direction)])
        agent.time_before_turn = int(agent.model.nprandom.exponential(agent.p.time_period))
        agent.time_straight = 0
        return new_vel
    else:
        agent.time_straight += 1
        return old_vel
