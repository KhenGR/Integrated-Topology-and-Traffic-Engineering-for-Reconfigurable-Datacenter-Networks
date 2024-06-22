from evaluation_Functions import *
import numpy as np
import matplotlib.pyplot as plt
from multi_proc import *
import time
import json


#import multiprocessing
class json_serialize(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    n = 8
    test_types = ("flow_number", "large_flow_ratio", "large_flow_load")
    #print(multiprocessing.cpu_count())
    x_values = power_range(4, 4 * n * n, 1.3)
    net = NetworkEval(n=n)
    start_time = time.perf_counter()
    #full_results = multi_run_tests(net_curr, 0.2, 0.7, x_values, 7, 28, test_types[0])
    x_values = np.linspace(0.05, 0.95, 19)
    full_results = multi_run_tests(net,0.2 , x_values, 30, 7, 28, test_types[2])
    #full_results = multi_run_tests(net_curr,x_values , 0.7, 10, 7, 28, test_types[1])
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    if n == 64:
        with open(f"test_res\\n64_test_total_flows_LR02_LLR07_date1906.json", 'w') as f:
            json.dump(full_results, f, sort_keys=True, indent=4,
                      ensure_ascii=False, cls=json_serialize)

    results = full_results["mean_res"]
    name_list = ("DA", "ROT", "PIV")
    for i, row in enumerate(np.transpose(results)):
        plt.plot(x_values, 1 / row, label=f'Curve {name_list[i]}', marker='o', linestyle='-', linewidth=2)

    #plt.xscale('log')
    # Add labels and title
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Curves from Matrix Rows')
    plt.legend()

    plt.show()
# net_curr = NetworkEval(n=64)
# bir = BirkDecomp()
#p_mat = traffic_generator(3, 7, 0.7, net_curr.n, 0.01)
# (p, al)=bir.birk_decomp(p_mat,0.001)
#[100,200,300,400,500,1000,2000]


#resi1 = run_tests_flow_number(net_curr, 0.2,0.7,x_values)
#resi2 = run_tests_flow_number(net_curr, 0.2,0.7,x_values)

#print(power_range(64, 20000, 1.2))
#results1=[d["res"] for d in resi1]
#results2=[d["res"] for d in resi2]
#results=[[2.3199939194375285, 1.9374882189102116, 1.246880635977973], [2.6999925928778223, 1.9374856487007812, 1.353024329568683], [2.8499926805823548, 1.9374858186283124, 1.4294522996670025], [2.909992584852229, 1.937485633151193, 1.4558973835975895], [2.9599925584390134, 1.937485581975589, 1.4727744137102814]]

#print(results)
