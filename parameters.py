import agentpy as ap
import numpy as np

""""""""""""""""""""
""" Main Params """
""""""""""""""""""""

def basic_parameters(faulty_scenario, tp, fp):
    """ Sort out population """
    total_pop = 20
    if faulty_scenario == "NF":
        healthy_pop = total_pop
        faulty_pop = 0
    else:
        healthy_pop = total_pop - int(total_pop/10)
        faulty_pop = int(total_pop/10)

    """ Sort out CTM-mitigation """
    if faulty_scenario == "MF":
        search_rate = 20
    else:
        search_rate = 2000

    # Define basic parameters
    parameters = {
        'size': 200,
        'seed': ap.IntRange(0, 10000),
        'fill_ratio' : 0.25,
        'steps': 1000,
        'ndim': 2,
        'healthy_population': healthy_pop,
        'faulty_population' : faulty_pop,
        'detection_radius' : 50,
        'faulty_search_rate' : search_rate,
        'double_check_rate' : 10,
        'true_positive' : tp,
        'false_positive': fp,
        'speed' : 2,
        'record_positions' : False,
        'movement_type' : 'random_walk',
        'time_period' : 50
    }
    return parameters

""""""""""""""""""""""""
""" Opinion Params """
""""""""""""""""""""""""

def pooling_parameters():
    parameters = {
        'opinion_updating_strategy' : 'pooling',
        'tau_evidence' : 30,
        'tau_sharing' : 20,
        'alpha' : 0.1,
        'w' : 1,
    }
    return parameters

def bbots_parameters():
    parameters = {
        'opinion_updating_strategy' : 'bbots',
        'tau_evidence' : 30,
        'tau_sharing' : 20,
        'alpha_0' : 2,
        'p_c' : 0.9,
        'u_plus' : True
    }
    return parameters

def dmmd_parameters():
    """
    Tau disseminate and exploration are the constants to control time spent in each state
    (before modulated by option quality)
    """
    parameters = {
        'opinion_updating_strategy' : 'dmmd',
        "tau_disseminate" : 90,
        "tau_exploration" : 30
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
        'time_period' : 40
    }
    return parameters

""""""""""""
""" Rest """
""""""""""""

def define_parameters(golden_params):
    """
    Define parameters for model
    """
    parameters = basic_parameters(*golden_params[1:])
    parameters.update(opinion_parameters(golden_params[0]))
    return parameters

def opinion_parameters(opinion_updating_strategy):
    opinion_parameters = {
        'SProdOp' : pooling_parameters,
        'BBots' : bbots_parameters,
        'DMMD' : dmmd_parameters
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