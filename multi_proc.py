#from multiprocessing #import Process
import multiprocessing
from evaluation_Functions import  *

def multi_run_tests_flow_number(net, large_ratio,large_load_ratio,x_values,processes_num,test_num):
    if not type(processes_num) is int:
        raise TypeError("Only integers are allowed")


    results= []
    if processes_num>1:
        # Create a pool of worker processes
        with multiprocessing.Pool(processes=processes_num) as pool:
            # Use pool.map to apply function to each element in the list
            same_arr= [(net, large_ratio, large_load_ratio, x_values)]*test_num
            results= pool.starmap(run_tests_flow_number, same_arr)
    else:
        #run each test with a single core.
        for i in range(test_num):
            results.append(run_tests_flow_number(net, large_ratio, large_load_ratio, x_values))



    # get the results
    reso=[]
    for i in range(len(results)):
        reso.append( [d["res"] for d in results[i]])
    resoreso = np.mean(np.array(reso), axis=0)
    return {"parameters":  net.get_all_parms()|{"large_ratio":large_ratio,"large_load_ratio":large_load_ratio,"Number_of_tests":test_num
            ,"List_of_tested_vals":x_values,"function_name":"multi_run_tests_flow_number"},
    "mean_res":resoreso, "full_result":reso}

# if __name__ == '__main__':
#     n = 8
#     x_values = power_range(4, 4 * n, 1.3)
#     net = network_eval(n=n)
#     full_results = multi_run_tests_flow_number(net, n, 0.2, 0.7, x_values, 4, 7)
#     results = full_results["mean_res"]
#     print(results)
