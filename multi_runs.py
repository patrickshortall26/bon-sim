from bts.simulation.model import Model, run_exp
from parameters import define_parameters
import _pickle as pickle

def main():
    """
    Define parameters, run simulations, and save as pickle
    """
    parameters = define_parameters()
    results = run_exp(Model, parameters, 100)
    # Save as pickle
    pickle.dump(results, file = open("results.pkl", "wb"))

if __name__ == "__main__":
    main()