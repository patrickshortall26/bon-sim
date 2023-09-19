from bts.simulation.model import Model, run_sim
from bts.simulation.animation import animate
from parameters import movement_parameters, opinion_parameters

def basic_parameters():
    parameters = {
        'size': 500,
        'steps': 1000,
        'ndim': 2,
        'healthy_population': 50,
        'faulty_population' : 0,
        'detection_radius' : 20,
        'faulty_search_rate' : 0.05,
        'detection_chance' : 0.8,
        'speed' : 3,
        'movement_type' : 'random_walk',
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

def main():
    """
    Define parameters, run simulation, and animate
    """
    parameters = define_parameters()
    model, results = run_sim(Model, parameters)
    animate(model, results)

if __name__ == "__main__":
    main()