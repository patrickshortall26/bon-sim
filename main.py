from bts.sim_setup import Model, run_sim
from bts.sim_animation import animate

def define_parameters():
    """
    Define parameters for model
    """
    parameters2D = {  
        'size': 50,
        'seed': 123,
        'steps': 100,
        'ndim': 2,
        'population': 100,
        'inner_radius': 3,
        'outer_radius': 10,
        'cohesion_strength': 0.01,
        'separation_strength': 0.1,
        'alignment_strength': 0.05,
    }
    return parameters2D

def main():
    """
    Define parameters, run simulation, and animate
    """
    parameters = define_parameters()
    model, results = run_sim(Model, parameters)
    animate(model, results)

if __name__ == "__main__":
    main()