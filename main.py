from bts.simulation.model import Model, run_sim
from bts.simulation.animation import animate
from parameters import movement_parameters, opinion_parameters

def basic_parameters():
    parameters = {
        'size': 500,
        'steps': 500,
        'ndim': 2,
        'healthy_population': 50,
        'faulty_population' : 50,
        'movement_type' : 'random_walk',
        'opinion_updating_strategy' : 'pooling',
        'speed' : 3
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