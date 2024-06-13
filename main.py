from traficGen import *
from julia_birkDecomp import birkDecomp
import time
import matplotlib.pyplot as plt




n=5
bir=birkDecomp()
#start_time = time.time()
perm_matrix = traffic_generator(2,3,0.95,n,0.01)
print(perm_matrix)
#end_time = time.time()
#elapsed_time = end_time - start_time
#print(f"Elapsed time: {elapsed_time} seconds")
#print(perm_matrix)
#for i in range(n):
# print(np.sum(perm_matrix[i]))
array = np.array([1, 2, 3, 4, 5])
cumulative_sum = np.cumsum(array)
print(cumulative_sum)
cumulative_sum = np.cumsum(array+1.1)
print(cumulative_sum)
#(a, w) = bir.birk_decomp(perm_matrix)
#print("hello")
#print(w)
# flat_mat = perm_matrix.flatten()
# print(flat_mat)
# plt.hist(flat_mat, bins=50,  density=True, alpha=0.7, color='blue', edgecolor='black')
# plt.title('Customized Histogram of Normally Distributed Data')
# plt.xlabel('Value')
# plt.ylabel('Density')

# Display the histogram
#plt.show()