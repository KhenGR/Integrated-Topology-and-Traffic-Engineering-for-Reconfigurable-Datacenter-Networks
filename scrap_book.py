import numpy as np
from traficGen import *
from julia_birkDecomp import birkDecomp
from multi_proc import  *
from traficGen import *

# large_load_ratio=0.7
# total_flows=2822
# large_number_ratio=0.2
# large_number = int(np.ceil(total_flows) *large_number_ratio)
# #In the case there are not enough large or small flows using the ratio, we set thier number to 1
# small_number = total_flows - large_number
#
#
# net= network_eval(n=64)
# resu = []
# for i in range(50):
#     p_mat = traffic_generator( large_number,small_number, large_load_ratio, net.n, 0.01)
#     resu.append(net.get_rotor_DCT(net.r * p_mat))
# print(np.mean(resu))

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

arr= [("dd",range(4),33)]*10
print(arr)