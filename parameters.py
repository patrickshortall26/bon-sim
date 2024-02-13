import agentpy as ap

""""""""""""""""""""
""" Main Params """
""""""""""""""""""""

def basic_parameters():
    # Define basic parameters
    parameters = {
        'size': 200,
        'seed': ap.IntRange(0, 10000),
        'fill_ratio' : 0.25,
        'steps': 1000,
        'ndim': 2,
        'healthy_population': 27,
        'faulty_population' : 3,
        'detection_radius' : 30,
        'faulty_search_rate' : 0.1,
        'true_positive' : 0.80,
        'false_positive': 0.01,
        'speed' : 1,
        'record_positions' : False
    }
    return parameters

""""""""""""""""""""""""
""" Opinion Params """
""""""""""""""""""""""""

def pooling_parameters():
    parameters = {
        'evidence_epsilon' : 0.02,
        'pooling_epsilon' : 0.02,
        'alpha' : 0.1,
        'w' : 1,
    }
    return parameters

def bbots_parameters():
    parameters = {
        'tau' : 20,
        'alpha_0' : 40,
        'p_c' : 0.99,
        'u_plus' : True
    }
    return parameters

def dmmd_parameters():
    parameters = {
        "dissemination_time" : 50,
        "disseminate_epsilon" : 0.10
    }
    return parameters

""""""""""""""""""""""""
""" Movement Params """
""""""""""""""""""""""""

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

""""""""""""
""" Rest """
""""""""""""

def choose_movement_type(parameters):
    movement_types = {'0' : 'random_walk', '1' : 'flocking'}
    movement_type = movement_types[input("Select movement type ('0' for random walk and '1' for flocking): ")]
    parameters.update({'movement_type' : movement_type})
    return parameters, movement_type

def choose_opinion_updating_strategy(parameters):
    opinion_updating_strategies = {'0' : 'pooling', '1' : 'bbots', '2' : 'dmmd'}
    opinion_updating_strategy = opinion_updating_strategies[input("Select movement type ('0' for pooling, '1' for bayes_bots, and '2' for DMMD): ")]
    parameters.update({'opinion_updating_strategy' : opinion_updating_strategy})
    return parameters, opinion_updating_strategy

def define_parameters():
    """
    Define parameters for model
    """
    parameters = basic_parameters()
    parameters.update({'record_positions' : True})
    parameters, movement_type = choose_movement_type(parameters)
    parameters, opinion_updating_strategy = choose_opinion_updating_strategy(parameters)
    parameters.update(movement_parameters(movement_type))
    parameters.update(opinion_parameters(opinion_updating_strategy))
    return parameters

def opinion_parameters(opinion_updating_strategy):
    opinion_parameters = {
        'pooling' : pooling_parameters,
        'bbots' : bbots_parameters,
        'dmmd' : dmmd_parameters
    }
    parameters = opinion_parameters[opinion_updating_strategy]()
    return parameters

def movement_parameters(movement_type):
    movement_parameters = {
        'flocking' : flocking_parameters,
        'random_walk' : random_walk_parameters
    }
    parameters = movement_parameters[movement_type]()
    return parameters