from numpy import random
import numpy as np
import scipy as sp
import time
def traffic_generator(nl, ns, cl, n, sigma):
    cs = 1 - cl
    large_ratio = cl / nl
    if nl > 0 and cl > 0:
        large_flows = np.random.normal(large_ratio, sigma*(large_ratio), int(nl))
    else:
        large_flows = np.zeros(int(nl))
    if nl > 0 and cl > 0:
        small_flows = np.random.normal(cs / ns, sigma*(cs / ns), int(ns))
    else:
        small_flows = np.zeros(ns)
    largeFlowsMatrix = np.zeros((n, n))
    for i in range(int(nl)):
        largeFlowsMatrix += large_flows[i]*random_permutation_matrix_no_dig(n)
    small_flows_matrix = np.zeros((n, n))
    for i in range(int(ns)):
        small_flows_matrix += small_flows[i]*random_permutation_matrix_no_dig(n)
    new_matrix = small_flows_matrix+largeFlowsMatrix
    new_matrix = n*new_matrix/np.sum(new_matrix)
    return new_matrix

def random_permutation_matrix_no_dig(size_of_perm):
    # Generate a random permutation of integers from 0 to n-1
    arr = random.permutation(size_of_perm)
    while np.any(arr == np.arange(size_of_perm)):
        arr = random.permutation(size_of_perm)

    # Create an n x n matrix filled with zeros
    permutation_matrix = np.zeros((size_of_perm, size_of_perm), dtype=int)

    # Place ones according to the permutation
    for i in range(size_of_perm):
        permutation_matrix[i, arr[i]] = 1

    return permutation_matrix

