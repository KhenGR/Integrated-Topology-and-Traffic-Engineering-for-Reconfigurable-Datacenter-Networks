#from multiprocessing #import Process
import multiprocessing
from evaluation_Functions import  *

def multi_run_tests_flow_number(net, n, large_ratio,large_load_ratio,x_values,processes_num,test_num):
    # Create a pool of worker processes
    results= []
    #x_values = power_range(4, 4 * 32*32 , 1.3)
    with multiprocessing.Pool(processes=processes_num) as pool:
        # Use pool.map to apply compute_square to each element in the list
        for i in range(test_num):
            #results.append(pool.starmap(compute_square, [(i+1 ,list(range(1,7)))]))
            results.append(run_tests_flow_number(net, large_ratio,large_load_ratio,x_values))
    # get the results
    reso=[]
    for i in range(len(results)):
        reso.append( [d["res"] for d in results[i]])
    resoreso = np.mean(np.array(reso), axis=0)
   # print(resoreso)
    return {"parameters":  net.get_all_parms()|{"large_ratio":large_ratio,"large_load_ratio":large_load_ratio,"Number_of_tests":test_num
            ,"List_of_tested_vals":x_values,"function_name":"multi_run_tests_flow_number"},
    "mean_res":resoreso, "full_result":reso}

#if __name__ == '__main__':

