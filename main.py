from bts.simulation.model import Model, run_sim, run_exp
from bts.visualisation.animation import animate
from parameters import define_parameters
import _pickle as pickle

def multi_run():
    """
    Define parameters, run simulations, and save as pickle
    """
    parameters = define_parameters()
    results = run_exp(Model, parameters, 100)
    # Save as pickle
    pickle.dump(results, file = open("results.pkl", "wb"))

def single_run():
    """
    Define parameters, run simulation, and animate
    """
    parameters = define_parameters()
    model, results = run_sim(Model, parameters)
    # Animate results
    animate(model, results)

def main():
    run_types = {'1' : single_run, '2' : multi_run}
    run_type = input("Key in '0' for single run or '1' for multi runs: ")
    run_types[run_type]()


if __name__ == "__main__":
    main()