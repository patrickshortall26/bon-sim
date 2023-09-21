from bts.simulation.model import Model, run_sim
from bts.visualisation.animation import animate
from parameters import define_parameters

def main():
    """
    Define parameters, run simulation, and animate
    """
    parameters = define_parameters()
    model, results = run_sim(Model, parameters)
    # Animate results
    animate(model, results)

if __name__ == "__main__":
    main()