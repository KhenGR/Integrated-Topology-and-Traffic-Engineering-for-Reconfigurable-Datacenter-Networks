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
x = {'a': 1, 'b': 2}
y = {'b': 3, 'c': 4,"t":44}
z = x | y
print(z)