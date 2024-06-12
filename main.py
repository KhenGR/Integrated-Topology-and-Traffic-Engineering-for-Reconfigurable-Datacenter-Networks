from traficGen import *
from julia_birkDecomp import birkDecomp
import time
import matplotlib.pyplot as plt
n=64
bir=birkDecomp()
start_time = time.time()
perm_matrix = traffic_generator(100,12,0.95,n,0.01)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")
#print(perm_matrix)
#for i in range(n):
   # print(np.sum(perm_matrix[i]))
(a, w) = bir.birk_decomp(perm_matrix, 0.001)
print("hello")
print(w)
flat_mat = perm_matrix.flatten()
print(flat_mat)
plt.hist(flat_mat, bins=50,  density=True, alpha=0.7, color='blue', edgecolor='black')
plt.title('Customized Histogram of Normally Distributed Data')
plt.xlabel('Value')
plt.ylabel('Density')

# Display the histogram
plt.show()