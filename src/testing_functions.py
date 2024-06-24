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
    #Remove the decimal point
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
    This function runs the expiremnet
    :param directory:
    :param large_ratio:
    :param large_load_ratio:
    :param n:
    :param rd:
    :param r:
    :param given_range:
    :return:
    """
    net = NetworkEval(n=n, rd=rd, r=r)
    (start, stop, coff) = given_range
    x_values = power_range(start, stop, coff)
    x_values = [np.ceil(x) for x in x_values]
    full_results = multi_run_tests(net, large_ratio, large_load_ratio,
                                   x_values, processor_to_use, number_of_runs, test_types[0])
    with open(os.path.join(directory, f"test_{test_types[0]}_LR{__float_as_string(large_ratio)}"
                                      f"_LLR{__float_as_string(large_load_ratio)}_n{__float_as_string(n)}.json"), 'w') as f:
        json.dump(full_results, f, sort_keys=True, indent=4,
                  ensure_ascii=False, cls=JsonSerialize)


def run_test_of_large_flow_load_change(directory,
                                       large_ratio=0.2,
                                       large_flow_number=64,
                                       n=64,
                                       rd=0.01,
                                       r=10000000000,
                                       given_range=(0.05, 0.95, 19)
                                       ):
    net = NetworkEval(n=n, rd=rd, r=r)
    (start, stop, steps) = given_range
    x_values = np.linspace(start, stop, steps)
    full_results = multi_run_tests(net, large_ratio, x_values,
                                   large_flow_number, processor_to_use, number_of_runs, test_types[2])
    with open(os.path.join(directory, f"test_{test_types[2]}_LR{__float_as_string(large_ratio)}"
                                      f"_FN{__float_as_string(large_flow_number)}_n{__float_as_string(n)}.json"), 'w') as f:
        json.dump(full_results, f, sort_keys=True, indent=4,
                  ensure_ascii=False, cls=JsonSerialize)


def run_test_of_large_flow_ratio_change(directory,
                                        large_load_ratio=0.7,
                                        large_flow_number=64,
                                        n=64,
                                        rd=0.01,
                                        r=10000000000,
                                        given_range=(0.05, 0.95, 19)
                                        ):
    net = NetworkEval(n=n, rd=rd, r=r)
    (start, stop, steps) = given_range
    x_values = np.linspace(start, stop, steps)
    full_results = multi_run_tests(net, x_values, large_load_ratio,
                                   large_flow_number, processor_to_use, number_of_runs, test_types[1])
    with open(os.path.join(directory, f"test_{test_types[1]}_LLR{__float_as_string(large_load_ratio)}"
                                      f"_FN{__float_as_string(large_flow_number)}_n{__float_as_string(n)}.json"), 'w') as f:
        json.dump(full_results, f, sort_keys=True, indent=4,
                  ensure_ascii=False, cls=JsonSerialize)


number_of_runs = 28
processor_to_use = multiprocessing.cpu_count() - 1
test_types = ("flow_number", "large_flow_ratio", "large_flow_load")

#if __name__ == '__main__':
#n = 64
#main test
#run_test_of_total_flow_number_change(0.2, 0.7,n=8)
# #Test large flow load variation
# #spars
#run_test_of_large_flow_load_change(0.2, 64)
# #dense
#run_test_of_large_flow_load_change(0.2, 3000)
# # Test large flow load variation
# # spars
#run_test_of_large_flow_ratio_change(large_load_ratio=0.7, large_flow_number=64)
# # dense
#run_test_of_large_flow_ratio_change(large_load_ratio=0.7, large_flow_number=3000)
