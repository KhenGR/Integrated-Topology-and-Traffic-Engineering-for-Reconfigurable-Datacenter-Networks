
from evaluation_Functions import  *
import numpy as np
import matplotlib.pyplot as plt

def run_tests_flow_number(net, large_ratio,large_load_ratio,total_flows_range):
    res_list = []
    for i in total_flows_range:
        total_flows = i
        large_number = np.ceil(total_flows) *large_load_ratio
        #In the case there are not enough large or small flows using the ratio, we set thier number to 1
        if large_number == 0:
            large_number=1
        small_number = total_flows - large_number
        if small_number == 0:
            small_number = 1
        perm_matrix = traffic_generator(large_number, small_number, large_load_ratio, net.n, 0.01)
        temp_res = net.test_four_algs(perm_matrix)
        res_list.append(temp_res.copy())
    return  res_list

def power_range(a, b, c):
    num_steps = int(np.floor(np.log(b / a) / np.log(c))) + 1
    # Generate the exponents
    exponents = np.arange(0, num_steps)
    # Generate the sequence using logspace
    result = a * np.power(c, exponents)
    # Convert the result to a list
    return result.tolist()


net = network_eval(n=32)
bir = birkDecomp()
p_mat = traffic_generator(3, 70, 0.7, net.n, 0.01)
(p, al)=bir.birk_decomp(p_mat)
(p, al)=bir.birk_decomp(p_mat)
#[100,200,300,400,500,1000,2000]
x_values = power_range(10, 2000, 1.3)
resi = run_tests_flow_number(net, 0.2,0.7,x_values)
#print(power_range(64, 20000, 1.2))
results=[d["res"] for d in resi]
#results=[[2.3199939194375285, 1.9374882189102116, 1.246880635977973], [2.6999925928778223, 1.9374856487007812, 1.353024329568683], [2.8499926805823548, 1.9374858186283124, 1.4294522996670025], [2.909992584852229, 1.937485633151193, 1.4558973835975895], [2.9599925584390134, 1.937485581975589, 1.4727744137102814]]

print(results)

name_list = ("DA","ROT","PIV")
for i, row in enumerate(np.transpose(results)):
    plt.plot(x_values,1/row, label=f'Curve {name_list[i]}', marker='o', linestyle='-', linewidth=2)

plt.xscale('log')
# Add labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Curves from Matrix Rows')
plt.legend()

plt.show()
# large_ratio=0.2
# total_flows=100
# large_number=np.ceil(total_flows) *large_ratio
# small_number = total_flows-large_number
# large_load_ratio=0.8
# perm_matrix = traffic_generator(large_number, small_number, large_load_ratio, net.n, 0.01)
# print(net.test_four_algs(perm_matrix))



#
# n=5
# bir=birkDecomp()
# #start_time = time.time()
# perm_matrix = traffic_generator(2,3,0.95,n,0.01)
# print(perm_matrix)
# #end_time = time.time()
# #elapsed_time = end_time - start_time
# #print(f"Elapsed time: {elapsed_time} seconds")
# #print(perm_matrix)
# #for i in range(n):
# # print(np.sum(perm_matrix[i]))
# array = np.array([1, 2, 3, 4, 5])
# cumulative_sum = np.cumsum(array)
# print(cumulative_sum)
# cumulative_sum = np.cumsum(array+1.1)
# print(cumulative_sum)
#
# list_to_sort = ['a', 'b', 'c', 'd']
# order_list = [3, 1, 4, 2]
#
# # Pair elements of both lists
# paired_list = list(zip(order_list, list_to_sort))
#
# # Sort the pairs based on the first element (order_list)
# sorted_pairs = sorted(paired_list)
#
# # Extract the sorted elements
# sorted_list = [element for _, element in sorted_pairs]
#
# print(sorted_list)
# #(a, w) = bir.birk_decomp(perm_matrix)
# #print("hello")
# #print(w)
# # flat_mat = perm_matrix.flatten()
# # print(flat_mat)
# # plt.hist(flat_mat, bins=50,  density=True, alpha=0.7, color='blue', edgecolor='black')
# # plt.title('Customized Histogram of Normally Distributed Data')
# # plt.xlabel('Value')
# # plt.ylabel('Density')
#
# # Display the histogram
# #plt.show()