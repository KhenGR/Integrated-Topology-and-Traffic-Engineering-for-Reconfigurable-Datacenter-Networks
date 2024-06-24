# This file contains functions which will be used to run the experiments in the paper
from src.multi_proc import *
import json
import os


class JsonSerialize(json.JSONEncoder):
    """"This class is used to serialize a dict into a jason, when the dict has an ndarray"""

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def __float_as_string(number):
    """
 :param number:
 :return: string
 Convert :param number to a string without the decimal point
   """
    number_str = str(number)
    # Remove the decimal point
    if '.' in number_str:
        number_str = number_str.replace('.', '')
    return number_str


def run_test_of_total_flow_number_change(directory,
                                         large_ratio=0.2,
                                         large_load_ratio=0.7,
                                         n=64,
                                         rd=0.01,
                                         r=10000000000,
                                         given_range=(4, 16384, 1.3)
                                         ):
    """
    This function tests our three systems with different total flow numbers and runs this for `number_of_runs` times
    :param directory: directory to save the result to
    :param large_ratio:large flow number ratio, that this large_flow_num= np.ceil(large_ratio*total_flows)
    :param large_load_ratio: the ratio of the load of the large flows
    :param n: number of nodes\network size
    :param rd: Demand aware reconfiguration time
    :param r: transmission rate
    :param given_range: (start, end, coefficients) for the `power_range` function
    :return: Nothing. Writes results to file
    """
    net = NetworkEval(n=n, rd=rd, r=r)
    (start, stop, coff) = given_range
    x_values = power_range(start, stop, coff)
    x_values = [np.ceil(x) for x in x_values]
    full_results = multi_run_tests(net, large_ratio, large_load_ratio,
                                   x_values, processor_to_use, number_of_runs, test_types[0])
    with open(os.path.join(directory, f"test_{test_types[0]}_LR{__float_as_string(large_ratio)}"
                                      f"_LLR{__float_as_string(large_load_ratio)}_n{__float_as_string(n)}.json"),
              'w') as f:
        json.dump(full_results, f, sort_keys=True, indent=4,
                  ensure_ascii=False, cls=JsonSerialize)


def run_test_of_large_flow_load_change(directory,
                                       large_ratio=0.2,
                                       flow_number=64,
                                       n=64,
                                       rd=0.01,
                                       r=10000000000,
                                       given_range=(0.05, 0.95, 19)
                                       ):
    """
    This function tests our three systems with different large flow load values and runs this for `number_of_runs` times
    :param directory: directory to save the result to
    :param large_ratio:large flow number ratio, that this large_flow_num= np.ceil(large_ratio*total_flows)
    :param flow_number: the total number of flows
    :param n: number of nodes\network size
    :param rd: Demand aware reconfiguration time
    :param r: transmission rate
    :param given_range: (start, end, steps) for the `np.linspace` function
    :return: Nothing. Writes results to file
    """
    net = NetworkEval(n=n, rd=rd, r=r)
    (start, stop, steps) = given_range
    x_values = np.linspace(start, stop, steps)
    full_results = multi_run_tests(net, large_ratio, x_values,
                                   flow_number, processor_to_use, number_of_runs, test_types[2])
    with open(os.path.join(directory, f"test_{test_types[2]}_LR{__float_as_string(large_ratio)}"
                                      f"_FN{__float_as_string(flow_number)}_n{__float_as_string(n)}.json"), 'w') as f:
        json.dump(full_results, f, sort_keys=True, indent=4,
                  ensure_ascii=False, cls=JsonSerialize)


def run_test_of_large_flow_ratio_change(directory,
                                        large_load_ratio=0.7,
                                        flow_number=64,
                                        n=64,
                                        rd=0.01,
                                        r=10000000000,
                                        given_range=(0.05, 0.95, 19)
                                        ):
    """
    This function tests our three systems with different large flow number ratio values and runs this for
     `number_of_runs` times
    :param directory: directory to save the result to
    :param large_load_ratio:the ratio of the load of the large flows
    :param flow_number: the total number of flows
    :param n: number of nodes / network size
    :param rd: Demand aware reconfiguration time
    :param r: transmission rate
    :param given_range: (start, end, steps) for the `np.linspace` function
    :return: Nothing. Writes results to file
    """
    net = NetworkEval(n=n, rd=rd, r=r)
    (start, stop, steps) = given_range
    x_values = np.linspace(start, stop, steps)
    full_results = multi_run_tests(net, x_values, large_load_ratio,
                                   flow_number, processor_to_use, number_of_runs, test_types[1])
    with open(os.path.join(directory, f"test_{test_types[1]}_LLR{__float_as_string(large_load_ratio)}"
                                      f"_FN{__float_as_string(flow_number)}_n{__float_as_string(n)}.json"), 'w') as f:
        json.dump(full_results, f, sort_keys=True, indent=4,
                  ensure_ascii=False, cls=JsonSerialize)


number_of_runs = 28
processor_to_use = multiprocessing.cpu_count() - 1
test_types = ("flow_number", "large_flow_ratio", "large_flow_load")
