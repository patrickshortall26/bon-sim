from bts.sim_setup import Model, run_sim
from bts.sim_animation import animate

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
    }
    return parameters


def movement_parameters(movement_type):
    movement_parameters = {
        'flocking' : flocking_parameters,
        'random_walk' : random_walk_parameters
    }
    parameters = movement_parameters[movement_type]()
    return parameters

def basic_parameters():
    parameters = {
        'size': 500,
        'seed': 123,
        'steps': 500,
        'ndim': 2,
        'population': 50,
        'movement_type' : 'random_walk',
        'speed' : 2
    }
    return parameters

def define_parameters():
    """
    Define parameters for model
    """
    parameters = basic_parameters()
    movement_type = parameters['movement_type']
    parameters.update(movement_parameters(movement_type))
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