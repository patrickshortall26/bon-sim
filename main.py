from bts.simulation.model import Model, run_sim, run_exp
from bts.visualisation.animation import animate
from parameters import define_parameters
import _pickle as pickle

def get_ttcs(results):
    """
    Get the time to consensus for each of the results
    """
    return results.reporters.loc[results.reporters['Correct decision?'] == True, 'Time to consensus']

def get_dict_results(results, results_filename):
    Results = {'TTC' : {}, 'parameters' : None}
    Results['TTC'][results_filename] = get_ttcs(results)
    Results['parameters'] = results.parameters.constants
    return Results

def multi_runs():
    """
    Define parameters, run simulations, and save as pickle
    """
    decisions_strategies = ["SProdOp", "BBots", "DMMD"]

    faulty_scenarios = ['NF', 'F', 'MF'] # Order as in boxplot

    # Parameter sweeps
    faulty_search_rates = [10, 20, 30, 40, 50] # or [20, 40, 60, 80, 100]
    double_check_rates = [5, 10, 15, 20, 25] # or [10, 20, 30, 40, 50]
    tps_fps = [(0.8,0.01), (0.84,0.02), (0.88,0.03), (0.92,0.04), (0.96,0.05)] # Sensitivity
    mus = [0.001, 0.011, 0.021, 0.031, 0.041]

    n_runs = 1000

    for strategy in decisions_strategies:

        # Each of the faulty scenarios
        for faulty_scenario in faulty_scenarios:
            break
            golden_params = [strategy, faulty_scenario, 20, 10, 0.88, 0.03, 0.001]
            parameters = define_parameters(golden_params)
            results = run_exp(Model, parameters, n_runs)
            results_filename = f"Results/Fault_scenarios/{strategy}-{faulty_scenario}"
            dict_results = get_dict_results(results, results_filename)
            # Save as pickle
            pickle.dump(dict_results, file = open(results_filename, "wb"))

        # PARAMETER SWEEPS
            
        # Faulty search rate
        for faulty_search_rate in faulty_search_rates:
            break
            golden_params = [strategy, 'MF', faulty_search_rate, 10, 0.88, 0.03, 0.001]
            parameters = define_parameters(golden_params)
            results = run_exp(Model, parameters, n_runs)
            results_filename = f"Results/FSR/{strategy}-FSR-{faulty_search_rate}"
            dict_results = get_dict_results(results, results_filename)
            # Save as pickle
            pickle.dump(dict_results, file = open(results_filename, "wb"))
            
        # Double check rate
        for double_check_rate in double_check_rates:
            break
            golden_params = [strategy, 'MF', 20, double_check_rate, 0.88, 0.03, 0.001]
            parameters = define_parameters(golden_params)
            results = run_exp(Model, parameters, n_runs)
            results_filename = f"Results/DCR/{strategy}-DCR-{double_check_rate}"
            dict_results = get_dict_results(results, results_filename)
            # Save as pickle
            pickle.dump(dict_results, file = open(results_filename, "wb"))

        # Sensitivity
        for tp_fp in tps_fps:
            break
            tp = tp_fp[0]
            fp = tp_fp[1]
            golden_params = [strategy, 'MF', 20, 10, tp, fp, 0.001]
            parameters = define_parameters(golden_params)
            results = run_exp(Model, parameters, n_runs)
            results_filename = f"Results/Sensitivity/{strategy}-{int(tp*100)}-{int(fp*100)}"
            dict_results = get_dict_results(results, results_filename)
            # Save as pickle
            pickle.dump(dict_results, file = open(results_filename, "wb"))
        
        # mu (learning rate)
        for mu in mus:
            golden_params = [strategy, 'MF', 20, 10, 0.88, 0.03, mu]
            parameters = define_parameters(golden_params)
            results = run_exp(Model, parameters, n_runs)
            results_filename = f"Results/Mu/{strategy}-Mu-{int(mu*1000)}"
            dict_results = get_dict_results(results, results_filename)
            # Save as pickle
            pickle.dump(dict_results, file = open(results_filename, "wb"))

def single_run():
    """
    Define parameters, run simulation, and animate
    """
    opinion_updating_strategies = {'0' : 'SProdOp', '1' : 'BBots', '2' : 'DMMD'}
    opinion_updating_strategy = opinion_updating_strategies[input("Select opinion updating strategy ('0' for SProdOp, '1' for BBots, and '2' for DMMD): ")]
    golden_params = [opinion_updating_strategy, 'MF', 20, 10, 0.88, 0.03, 0.001]
    parameters = define_parameters(golden_params)
    parameters['record_positions'] = True
    model, results = run_sim(Model, parameters)
    # Animate results
    animate(model, results)

def main():
    run_types = {'1' : single_run, '2' : multi_runs}
    run_type = input("Key in '1' for single run or '2' for multi runs: ")
    run_types[run_type]()


if __name__ == "__main__":
    main()