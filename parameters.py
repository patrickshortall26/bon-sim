def basic_parameters():
    parameters = {
        'size': 500,
        'steps': 1000,
        'ndim': 2,
        'healthy_population': 50,
        'faulty_population' : 5,
        'detection_radius' : 30,
        'faulty_search_rate' : 0.0,
        'detection_chance' : 0.8,
        'speed' : 6,
        'movement_type' : 'flocking',
        'opinion_updating_strategy' : 'pooling'
    }
    return parameters

def define_parameters():
    """
    Define parameters for model
    """
    parameters = basic_parameters()
    movement_type = parameters['movement_type']
    opinion_updating_strategy = parameters['opinion_updating_strategy']
    parameters.update(movement_parameters(movement_type))
    parameters.update(opinion_parameters(opinion_updating_strategy))
    return parameters

def opinion_parameters(opinion_updating_strategy):
    opinion_parameters = {
        'pooling' : pooling_parameters
    }
    parameters = opinion_parameters[opinion_updating_strategy]()
    return parameters

def pooling_parameters():
    parameters = {
        'pooling_radius' : 30,
        'evidence_epsilon' : 0.02,
        'pooling_epsilon' : 0.02,
        'alpha' : 0.1,
        'w' : 1,
    }
    return parameters

def flocking_parameters():
    parameters = {
        'inner_radius': 30,
        'outer_radius': 100,
        'cohesion_strength': 0.005,
        'separation_strength': 0.1,
        'alignment_strength': 0.3
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