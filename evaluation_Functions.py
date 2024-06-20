import numpy as np

from traficGen import *
from julia_birkDecomp import birkDecomp


def power_range(a, b, c):
    num_steps = int(np.floor(np.log(b / a) / np.log(c))) + 1
    # Generate the exponents
    exponents = np.arange(0, num_steps)
    # Generate the sequence using logspace
    result = a * np.power(c, exponents)
    # Convert the result to a list
    return result.tolist()


def sort_list_by_other_list(order_list, list_to_sort, rev=False):
    paired_list = list(zip(order_list, list_to_sort))
    # Sort the pairs based on the first element (order_list)
    # print("in sort list")
    # print(paired_list)
    sorted_pairs = sorted(paired_list, key=lambda tup: tup[0], reverse=rev)
    # Extract the sorted elements
    sorted_list = [element for _, element in sorted_pairs]
    return sorted_list


def sparsity_mesure(M):
    non_zero = np.count_nonzero(M)
    total_val = np.prod(M.shape)
    sparsity = (total_val - non_zero) / total_val
    return sparsity


def var_dist_line(arr):
    """this function calculates the variation distance of one row of a matrix"""
    arr = np.array(arr)
    normalized_mat = arr / np.sum(arr)
    #This is always 1/len(arr) unless something is wrong
    mean = np.mean(normalized_mat)
    var_dist = np.sum(np.absolute([mean - j for j in normalized_mat])) / 2
    return var_dist


def var_dist_mat(M):
    """this function calculates the variation distance of a square matrix with zeros on the diagonal"""
    dim = len(M)
    no_zeros_mat = np.array([np.delete(mat, x) for mat, x, in zip(M, list(range(dim)))])
    var_dist = np.mean([var_dist_line(x) for x in no_zeros_mat])
    return var_dist


class network_eval:
    rd: float
    n: int
    r: float
    rr: float
    bir: birkDecomp

    def __init__(self, n=64, rr=0, rd=0.01, r=10000000000):
        self.rd = rd
        self.n = n
        self.r = r
        self.rr = rr
        self.bir = None  #birkDecomp()

    def get_all_parms(self):
        return {"n": self.n, "r": self.r, "rd": self.rd}

    def get_rotor_DCT(self, M):
        #Take maximal line sum
        row_sums = np.sum(M, axis=1)
        max_row_load = np.max(row_sums)
        # Take maximal element
        max_elem = np.max(M)
        constent_DCT = (2 - (2 / self.n)) * (1 / self.r) * max_row_load
        max_elem_DCT = (self.n - 1) * (1 / self.r) * max_elem
        return np.min((constent_DCT, max_elem_DCT))

    def pivot_alg_DCT(self, P_lis, alpha):
        sorted_alpha = np.array(sorted(alpha, reverse=True))
        sorted_P = sort_list_by_other_list(alpha, P_lis, rev=True)
        cumulative_DCT_DA = np.cumsum(sorted_alpha + self.rd)
        summrized_matrix = self.r * np.sum(sorted_P, axis=0)
        zeros_mat = np.zeros((self.n, self.n))
        cumulative_sums = []
        for i in range(len(sorted_P)):
            zeros_mat += self.r * sorted_P[i]
            cumulative_sums.append(zeros_mat.copy())
        cum_lis = [summrized_matrix - j for j in cumulative_sums]
        cumulative_DCT_rot = [self.get_rotor_DCT(j) for j in cum_lis]
        all_pivot_results = [i + j for i, j, in zip(cumulative_DCT_rot, cumulative_DCT_DA)]
        best_res_pivot = np.min(all_pivot_results)
        best_res_index = np.argmin(all_pivot_results)
        #{"DA":best_res_index+1, "RR":len(alpha)-1-best_res_index}
        return {"best_res_pivot": best_res_pivot, "piv_index": (best_res_index + 1, len(alpha) - 1 - best_res_index)}

    def test_four_algs(self, M, birk_epsilon=0.0001, index=1):
        #get the birkoff decompestion
        #bir = birkDecomp()
        (p, al) = self.bir.birk_decomp(M, birk_epsilon)

        trans_p = np.transpose(p)
        total_arrs = [np.transpose(np.mat(transP * al).reshape(self.n, self.n)) for transP, al, in zip(trans_p, al)]
        pivot_DCT_res_dict = self.pivot_alg_DCT(total_arrs, al)
        pivot_DCT = pivot_DCT_res_dict["best_res_pivot"]
        index_piv_res = pivot_DCT_res_dict["piv_index"]
        #Send to the rotor the possibliy slightly reduced matrix from the decomp
        new_m = np.sum(total_arrs, axis=0)
        rotor_DCT = self.get_rotor_DCT(self.r * new_m)

        #calculate the dct of DA system
        da_DCT = np.sum(al) + len(al) * self.rd
        return {"index": index, "res": [da_DCT, rotor_DCT, np.min((da_DCT, rotor_DCT, pivot_DCT))],
                "max": np.max(new_m), "var_dist": var_dist_mat(np.array(new_m)), "BvN_dist": len(al),
                "sparsity": sparsity_mesure(np.array(new_m)), "piv_div_res": index_piv_res}


def run_tests_flow_number(net, large_ratio, large_load_ratio, total_flows_range):
    res_list = []
    if net.bir == None:
        net.bir = birkDecomp()
    for i in total_flows_range:
        total_flows = i
        large_number = np.ceil(total_flows) * large_ratio
        #In the case there are not enough large or small flows using the ratio, we set thier number to 1
        if large_number == 0:
            large_number = 1
        small_number = total_flows - large_number
        if small_number == 0:
            small_number = 1
        perm_matrix = traffic_generator(large_number, small_number, large_load_ratio, net.n, 0.01)
        temp_res = net.test_four_algs(perm_matrix)
        res_list.append(temp_res.copy())
    return res_list


def run_tests_large_flow_load(net, large_ratio, large_load_ratio_range, total_flows):
    res_list = []
    if net.bir == None:
        net.bir = birkDecomp()
    for i in large_load_ratio_range:
        large_load_ratio = i
        large_number = np.ceil(total_flows * large_ratio)
        #In the case there are not enough large or small flows using the ratio, we set thier number to 1
        if large_number == 0:
            large_number = 1
        small_number = total_flows - large_number
        if small_number == 0:
            small_number = 1
        perm_matrix = traffic_generator(large_number, small_number, large_load_ratio, net.n, 0.01)
        temp_res = net.test_four_algs(perm_matrix)
        res_list.append(temp_res.copy())
    return res_list


def run_tests_large_flow_ratio(net, large_ratio_range, large_load_ratio, total_flows):
    res_list = []
    if net.bir is None:
        net.bir = birkDecomp()
    for i in large_ratio_range:
        large_ratio = i
        large_number = np.ceil(total_flows * large_ratio)
        #In the case there are not enough large or small flows using the ratio, we set thier number to 1
        if large_number == 0:
            large_number = 1
        small_number = total_flows - large_number
        if small_number == 0:
            small_number = 1
        perm_matrix = traffic_generator(large_number, small_number, large_load_ratio, net.n, 0.01)
        temp_res = net.test_four_algs(perm_matrix)
        res_list.append(temp_res.copy())
    return res_list
# def power_range(a, b, c):
#     num_steps = int(np.floor(np.log(b / a) / np.log(c))) + 1
#     # Generate the exponents
#     exponents = np.arange(0, num_steps)
#     # Generate the sequence using logspace
#     result = a * np.power(c, exponents)
#     # Convert the result to a list
#     return result.tolist()

#
# net = network_eval(n=64)
# perm_matrix = traffic_generator(3, 45, 0.95, net.n, 0.01)
# #print(net.test_four_algs(perm_matrix))
# bir = birkDecomp()
# (p, al) = bir.birk_decomp(perm_matrix, 0.00001)
# print(p)
# al=np.array(al)
# print("endline")
# res = np.transpose(p)
# res2 = [np.transpose(np.mat(res * al).reshape(net.n, net.n)) for res, al, in zip(res, al)]
# #print(res2[2])
# print(sorted(al))
# print(res2[2])
# print(res2[0] + res2[2])
# print("endline")
# print("endline")
#
# newM = np.sum(res2, axis=0)
#
# print(newM)
# print("endlin231e")
# zeros_mat = np.zeros((net.n,net.n))
#
# cumulative_sums = []
# for i in range(len(res2)):
#     zeros_mat+=res2[i]
#     cumulative_sums.append(zeros_mat.copy())
# print(cumulative_sums[0])
# print("endlin23fawfsde")
# cumlis =  [newM- ll for ll in cumulative_sums]
# print(res2[-1])
# #print(net.pivot_alg_DCT(res2,al))
#
# print (net.test_four_algs(perm_matrix))
