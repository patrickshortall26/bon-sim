
def flocking_parameters():
    parameters = {
        'inner_radius': 20,
        'outer_radius': 70,
        'cohesion_strength': 0.01,
        'separation_strength': 0.1,
        'alignment_strength': 0.05
    }
    return parameters

def random_walk_parameters():
    parameters = {
        'time_period' : 50
    }
    return parameters


def movement_parameters(movement_type):
    movement_parameters = {
        'flocking' : flocking_parameters,
        'random_walk' : random_walk_parameters
    }
    parameters = movement_parameters[movement_type]()
    return parameters