from multi_proc import  *
import time
import json

class json_serialize(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
n = 64
number_of_runs = 28

#set this to 1 in order to not use multiprocessing,
#Can be usfull for small calculations
processor_to_use = multiprocessing.cpu_count()-1


def  run_test_of_total_flow_number_change():
    net = network_eval(n=n)
    x_values = power_range(4, 4 *n *n,1.3)
    large_ratio = 0.2
    large_load_ratio = 0.7
    full_results = multi_run_tests_flow_number(net, large_ratio,large_load_ratio,x_values,7,number_of_runs)
    with open(f"test_res\\n64_test_total_flows_LR02_LLR07_date1906.json", 'w') as f:
        json.dump(full_results, f, sort_keys=True, indent=4,
                  ensure_ascii=False)
if __name__ == '__main__':
    run_test_of_total_flow_number_change()
    #print(multiprocessing.cpu_count())

