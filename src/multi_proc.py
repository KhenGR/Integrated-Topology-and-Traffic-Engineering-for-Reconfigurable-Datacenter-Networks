# This functions in file only implement running our experiments on several cores and getting the mean of the results
import multiprocessing
from src.evaluation_Functions import *


def return_dict_mean_res(key: str, result) -> dict:
    """
     takes a list with several values which are the results of several runs of the function and returns
     a dict with their mean to transfer forward
    :param key: a string which is a key to the
    :param result:
    :return:
    """
    arr = []
    for i in range(len(result)):
        arr.append([d[key] for d in result[i]])
    arr_mean = np.mean(np.array(arr), axis=0)
    return {key + "_mean": arr_mean}


def multi_run_tests(net: NetworkEval,
                    large_ratio: float | np.ndarray | list,
                    large_load_ratio: float | np.ndarray | list,
                    flow_number: float | np.ndarray | list,
                    processes_num: int, test_num: int,
                    test_type: str) -> dict:
    """
    This function runs the experiments from the paper using several cores if possible
    :param net: the NetworkEval object which contains the parameters of the network
    :param large_ratio: number of large flows
    :param large_load_ratio: ratio of the load of large flows (cs is the small flow load)
    :param flow_number: number of flows
    :param processes_num: the number processes to use
    :param test_num: the number of tests to run
    :param test_type: types of possible tests.
    :return: A result dict
    """
    if not type(processes_num) is int:
        raise TypeError("Only integers are allowed when setting the number of processes")
    results = []
    match test_type:
        # There are three possible tests possible here: flow_number, large_flow_load, and large_flow_ratio
        case "flow_number":
            x_values = flow_number
            if processes_num > 1:
                # Create a pool of worker processes
                with multiprocessing.Pool(processes=processes_num) as pool:
                    # Use pool.map to apply function to each element in the list
                    same_arr = [(net, large_ratio, large_load_ratio, x_values)] * test_num
                    results = pool.starmap(run_tests_flow_number, same_arr)
            else:
                # run each test with a single core.
                for i in range(test_num):
                    results.append(run_tests_flow_number(net, large_ratio, large_load_ratio, x_values))
        case "large_flow_load":
            x_values = large_load_ratio
            if processes_num > 1:
                # Create a pool of worker processes
                with multiprocessing.Pool(processes=processes_num) as pool:
                    same_arr = [(net, large_ratio, x_values, flow_number)] * test_num
                    results = pool.starmap(run_tests_large_flow_load, same_arr)
            else:
                for i in range(test_num):
                    results.append(run_tests_large_flow_load(net, large_ratio, x_values, flow_number))
        case "large_flow_ratio":
            x_values = large_ratio
            if processes_num > 1:
                # Create a pool of worker processes
                with multiprocessing.Pool(processes=processes_num) as pool:
                    same_arr = [(net, x_values, large_load_ratio, flow_number)] * test_num
                    results = pool.starmap(run_tests_large_flow_ratio, same_arr)
            else:
                for i in range(test_num):
                    results.append(run_tests_large_flow_ratio(net, x_values, large_load_ratio, flow_number))
        case _:
            raise TypeError("Only strings of the following types are allowed: flow_number, large_flow_ratio, "
                            "large_flow_load")
    # get the results
    # Builds the dictionary with each field
    reso = []
    # This is a three sized tuple, will need different treatment
    for i in range(len(results)):
        reso.append([d["res"] for d in results[i]])
    res_mean = np.mean(np.array(reso), axis=0)
    # Calculate the mean result for each run
    bvn_dis_mean = return_dict_mean_res("BvN_dist", results)
    sparsity_mean = return_dict_mean_res("sparsity", results)
    max_mean = return_dict_mean_res("max", results)
    var_mean = return_dict_mean_res("var_dist", results)
    piv_res_mean = return_dict_mean_res("piv_div_res", results)
    da_load_mean = return_dict_mean_res("da_load", results)
    return ({"parameters": net.get_all_parms() |
                           {"large_ratio": large_ratio,
                            "large_load_ratio": large_load_ratio,
                            "number_of_tests": test_num,
                            "List_of_tested_vals": x_values,
                            "test_name": test_type},
             "mean_res": res_mean,
             "full_result": reso}
            | bvn_dis_mean
            | sparsity_mean
            | max_mean
            | var_mean
            | piv_res_mean
            | da_load_mean)

# Result dict structure
# parameters: List of parameters used in the test
##          n: number of nodes\ network size
##          rd: Demand aware reconfiguration time
##          r: transmission rate
##          large_ratio: The ratio of the number of large flows of all flows
##          large_load_ratio: The ratio of the load of large flows
##          number_of_tests: The number of tests which were run
##          List_of_tested_vals: The tested values. This could represent the flow number, large flow load or large flow ratio
##          test_name: Which test was used to create this data set

# full_result: This is raw DCT result for our three systems.
# The list has a list for each of our 'number_of_tests' tetes,
# where each sublist has the same form as "mean_res". (Not used)

# In the following fields each element in position "i" is equivalent to an experiment with\
# List_of_tested_vals[i] in terms of tested parameter.
# And each result is the mean of "number_of_tests" results.
# mean_res: The mean DCT results for our three systems in the tuple ("BvN-sys", "RR-sys", "COMP-sys").
# bvn_dis_mean: The number of elements in the BvN decomposition (Not used)
# sparsity_mean: The sparsity of the tested traffic matrix
# max_mean: The maximal value of the tested traffic matrix
# var_mean: The variation distance value of the tested traffic matrix
# piv_res_mean: A tuple where each element represents the division of the pivot algorithm
# in terms of the number of permutations sent to da-sys or rr-sys where (da, rr) (Not used)
# da_load_mean:
#
