from bts.sim_setup import Model, run_sim
from bts.sim_animation import animate
from parameters import movement_parameters

def basic_parameters():
    parameters = {
        'size': 500,
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