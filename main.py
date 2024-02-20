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
    decisions_strategies = ["BBots"]

    faulty_scenarios = ['NF', 'F', 'MF'] # Order as in boxplot

    tps = [0.8, 0.84, 0.88, 0.92, 0.96] # bad --> good
    fps = [0.05, 0.04, 0.03, 0.02, 0.01] # bad --> good

    tps_fps = [(0.8,0.01), (0.84,0.02), (0.88,0.03), (0.92,0.04), (0.96,0.05)] # less sensitive --> more sensitive

    n_runs = 100

    for strategy in decisions_strategies:

        # faulty scenarios first
        for faulty_scenario in faulty_scenarios:
            golden_params = [strategy, faulty_scenario, 0.88, 0.3]
            parameters = define_parameters(golden_params)
            results = run_exp(Model, parameters, n_runs)
            results_filename = f"Results/fault_scenarios/{strategy}-{faulty_scenario}"
            dict_results = get_dict_results(results, results_filename)
            # Save as pickle
            pickle.dump(dict_results, file = open(results_filename, "wb"))
        
        break

        # Then do the parameter sweeps  
        # true positives
        for tp in tps:
            fp = 0.3
            golden_params = [strategy, faulty_scenario, tp, fp]
            parameters = define_parameters(golden_params)
            results = run_exp(Model, parameters, n_runs)
            results_filename = f"Results/tps/{strategy}-TP-{int(tp*100)}"
            dict_results = get_dict_results(results, results_filename)
            # Save as pickle
            pickle.dump(dict_results, file = open(results_filename, "wb"))

        # false positives
        for fp in fps:
            tp = 0.88
            golden_params = [strategy, faulty_scenario, tp, fp]
            parameters = define_parameters(golden_params)
            results = run_exp(Model, parameters, n_runs)
            results_filename = f"Results/fps/{strategy}-FP-{int(fp*100)}"
            dict_results = get_dict_results(results, results_filename)
            # Save as pickle
            pickle.dump(dict_results, file = open(results_filename, "wb"))

        # true positives
        for tp_fp in tps_fps:
            tp = tp_fp[0]
            fp = tp_fp[1]
            golden_params = [strategy, faulty_scenario, tp, fp]
            parameters = define_parameters(golden_params)
            results = run_exp(Model, parameters, n_runs)
            results_filename = f"Results/tps_fps/{strategy}-{int(tp*100)}-{int(fp*100)}"
            dict_results = get_dict_results(results, results_filename)
            # Save as pickle
            pickle.dump(dict_results, file = open(results_filename, "wb"))

def single_run():
    """
    Define parameters, run simulation, and animate
    """
    opinion_updating_strategies = {'0' : 'SProdOp', '1' : 'BBots', '2' : 'DMMD'}
    opinion_updating_strategy = opinion_updating_strategies[input("Select opinion updating strategy ('0' for SProdOp, '1' for BBots, and '2' for DMMD): ")]
    golden_params = [opinion_updating_strategy,'NF',0.88,0.3]
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