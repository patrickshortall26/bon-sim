def opinion_parameters(opinion_updating_strategy):
    opinion_parameters = {
        'pooling' : pooling_parameters
    }
    parameters = opinion_parameters[opinion_updating_strategy]()
    return parameters

def pooling_parameters():
    parameters = {
        'pooling_radius' : 20,
        'evidence_epsilon' : 0.05,
        'pooling_epsilon' : 0.03,
        'alpha' : 0.1,
        'w' : 10,
    }
    return parameters

def flocking_parameters():
    parameters = {
        'inner_radius': 20,
        'outer_radius': 70,
        'cohesion_strength': 0.01,
        'separation_strength': 0.2,
        'alignment_strength': 0.5
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