from bts.simulation.model import Model, run_sim, run_exp
from bts.visualisation.animation import animate
from parameters import define_parameters
import _pickle as pickle

def get_ttcs(results):
    """
    Get the time to consensus for each of the results
    """
    return results.reporters.loc[results.reporters['Decision'] == "Correct decision", 'Time to consensus']

def get_dict_results(results, results_filename):
    Results = {'TTC' : {}, 'parameters' : None}
    Results['TTC'][results_filename] = get_ttcs(results)
    return Results

def multi_run():
    """
    Define parameters, run simulations, and save as pickle
    """
    parameters = define_parameters()
    results_filename = input("Please give a filename to store results: ")
    results = run_exp(Model, parameters, 1000)
    dict_results = get_dict_results(results)
    # Save as pickle
    pickle.dump(dict_results, file = open(f"parameter_sweep/{results_filename}", "wb"))

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
    run_type = input("Key in '1' for single run or '2' for multi runs: ")
    run_types[run_type]()


if __name__ == "__main__":
    main()