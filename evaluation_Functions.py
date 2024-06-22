import numpy as np

from traficGen import *
from julia_birkDecomp import BirkDecomp


def power_range(a, b, c):
    """
    this gives a power range where each element is from
    {a,ca,c^2a,...,c^n*a}, where c^n*a<=b
    :param a: start of range
    :param b: maximal element of range
    :param c: factor
    :return: range of numbers
    """
    num_steps = int(np.floor(np.log(b / a) / np.log(c))) + 1
    # Generate the exponents
    exponents = np.arange(0, num_steps)
    # Generate the sequence using logspace
    result = a * np.power(c, exponents)
    # Convert the result to a list
    return result.tolist()


def sort_list_by_other_list(order_list, list_to_sort, rev=False):
    """
    sorts a list according the another list
    :param order_list: the list with the order
    :param list_to_sort: the list that is sorted
    :param rev: reverse, true false
    :return: list_to_sort but sorted by order_list
    """
    paired_list = list(zip(order_list, list_to_sort))
    # Sort the pairs based on the first element (order_list)
    sorted_pairs = sorted(paired_list, key=lambda tup: tup[0], reverse=rev)
    # Extract the sorted elements
    sorted_list = [element for _, element in sorted_pairs]
    return sorted_list


def sparsity_measure(m) -> float:
    """
    gets the sparsity of a matrix
    :param m: a matrix
    :return: sparsity float
    """
    non_zero = np.count_nonzero(m)
    total_val = np.prod(m.shape)
    sparsity = (total_val - non_zero) / total_val
    return sparsity


def var_dist_line(arr)-> float:
    """
    #this function calculates the variation distance of one row of a matrix
    :arr the array to calculate
    """
    arr = np.array(arr)
    normalized_mat = arr / np.sum(arr)
    #This is always 1/len(arr) unless something is wrong
    mean = np.mean(normalized_mat)
    var_dist = np.sum(np.absolute([mean - j for j in normalized_mat])) / 2
    return var_dist


def var_dist_mat(m):
    """this function calculates the variation distance of a square matrix with zeros on the diagonal"""
    dim = len(m)
    no_zeros_mat = np.array([np.delete(mat, x) for mat, x, in zip(m, list(range(dim)))])
    var_dist = np.mean([var_dist_line(x) for x in no_zeros_mat])
    return var_dist


class NetworkEval:
    rd: float
    n: int
    r: float
    rr: float
    bir: BirkDecomp

    def __init__(self, n=64, rr=0, rd=0.01, r=10000000000):
        """
        This initializes the class NetworkEval with the parameters used in the paper as default
        :param n: number of nodes\ network size
        :param rr: Round robin reconfiguration time
        :param rd: Demand aware reconfiguration time
        :param r: trans rate
        """
        self.rd = rd
        self.n = n
        self.r = r
        self.rr = rr
        self.bir = None  #BirkDecomp()

    def get_all_parms(self):
        """
        returns a dict with all parameters
        :return: a dict
        """
        return {"n": self.n, "r": self.r, "rd": self.rd}

    def get_rr_dct(self, m):
        """
        Gets the round robin dct
        :param m: a matrix
        :return: dct of rr system
        """
        #Take maximal line sum
        row_sums = np.sum(m, axis=1)
        max_row_load = np.max(row_sums)
        # Take maximal element
        max_elem = np.max(m)
        constent_DCT = (2 - (2 / self.n)) * (1 / self.r) * max_row_load
        max_elem_DCT = (self.n - 1) * (1 / self.r) * max_elem
        return np.min((constent_DCT, max_elem_DCT))

    def pivot_alg_DCT(self, p_lis, alpha):
        # new_index=np.where(np.array(alpha_new)<(self.rd/4))
        # alpha = alpha_new
        # p_lis = P_lis_new
        sorted_alpha = np.array(sorted(alpha, reverse=True))
        sorted_p = sort_list_by_other_list(alpha, p_lis, rev=True)
        cumulative_dct_da = np.cumsum(sorted_alpha + self.rd)
        summrized_matrix = self.r * np.sum(sorted_p, axis=0)
        zeros_mat = np.zeros((self.n, self.n))
        cumulative_sums = []
        for i in range(len(sorted_p)):
            zeros_mat += self.r * sorted_p[i]
            cumulative_sums.append(zeros_mat.copy())
        cum_lis = [summrized_matrix - j for j in cumulative_sums]
        cumulative_DCT_rot = [self.get_rr_dct(j) for j in cum_lis]
        all_pivot_results = [i + j for i, j, in zip(cumulative_DCT_rot, cumulative_dct_da)]
        best_res_pivot = np.min(all_pivot_results)
        best_res_index = np.argmin(all_pivot_results)
        #da_load = np.sum(sorted_alpha[0:best_res_index+1])
        #da_load = np.sum(sorted_p[0:best_res_index+1])
        #rr_load = np.sum(sorted_p[best_res_index+1:])
        #da_load = da_load / (rr_load+da_load)
        da_load = np.sum(sorted_alpha[0:best_res_index + 1])
        #{"DA":best_res_index+1, "RR":len(alpha)-1-best_res_index}
        return {"best_res_pivot": best_res_pivot,
                "piv_index": (best_res_index, len(alpha) - best_res_index),
                "da_load": da_load}

    def test_four_algs(self, M, birk_epsilon=0.00001, index=1):
        #get the birkoff decompestion
        #bir = BirkDecomp()
        (p, al) = self.bir.birk_decomp(M, birk_epsilon)

        trans_p = np.transpose(p)
        total_arrs = [np.transpose(np.mat(transP * al).reshape(self.n, self.n)) for transP, al, in zip(trans_p, al)]
        pivot_dct_res_dict = self.pivot_alg_DCT(total_arrs, al)
        pivot_dct = pivot_dct_res_dict["best_res_pivot"]
        index_piv_res = pivot_dct_res_dict["piv_index"]
        da_load = pivot_dct_res_dict["da_load"]
        #Send to the rotor the possibliy slightly reduced matrix from the decomp
        new_m = np.sum(total_arrs, axis=0)
        rotor_dct = self.get_rr_dct(self.r * new_m)
        #calculate the dct of DA system
        da_dct = np.sum(al) + len(al) * self.rd
        # Since we do not test the edge cases inside of the pivot_alg_DCT function,
        # we test them here for the load
        if da_dct <= pivot_dct and da_dct <= rotor_dct:
            da_load = 1
        elif rotor_dct <= pivot_dct and rotor_dct <= da_dct:
            da_load = 0
        return {"index": index, "res": [da_dct, rotor_dct, np.min((da_dct, rotor_dct, pivot_dct))],
                "max": np.max(new_m), "var_dist": var_dist_mat(np.array(new_m)), "BvN_dist": len(al),
                "sparsity": sparsity_measure(np.array(new_m)), "piv_div_res": index_piv_res, "da_load": da_load}


def run_tests_flow_number(net_curr, large_ratio, large_load_ratio, total_flows_range):
    res_list = []
    if net_curr.bir is None:
        net_curr.bir = BirkDecomp()
    for i in total_flows_range:
        total_flows = i
        large_number = np.ceil(np.ceil(total_flows) * large_ratio)
        #In the case there are not enough large or small flows using the ratio, we set thier number to 1
        # if large_number == 0:
        #     large_number = 1
        small_number = np.ceil(total_flows) - large_number
        if small_number == 0:
            small_number = 1
        perm_matrix = traffic_generator(large_number, small_number, large_load_ratio, net_curr.n, 0.01)
        temp_res = net_curr.test_four_algs(perm_matrix)
        res_list.append(temp_res.copy())
    return res_list


def run_tests_large_flow_load(net_curr, large_ratio, large_load_ratio_range, total_flows):
    res_list = []
    if net_curr.bir == None:
        net_curr.bir = BirkDecomp()
    for i in large_load_ratio_range:
        large_load_ratio = i
        large_number = np.ceil(total_flows * large_ratio)
        #In the case there are not enough large or small flows using the ratio, we set thier number to 1
        if large_number == 0:
            large_number = 1
        small_number = total_flows - large_number
        if small_number == 0:
            small_number = 1
        perm_matrix = traffic_generator(large_number, small_number, large_load_ratio, net_curr.n, 0.01)
        temp_res = net_curr.test_four_algs(perm_matrix)
        res_list.append(temp_res.copy())
    return res_list


def run_tests_large_flow_ratio(net_curr, large_ratio_range, large_load_ratio, total_flows):
    res_list = []
    if net_curr.bir is None:
        net_curr.bir = BirkDecomp()
    for i in large_ratio_range:
        large_ratio = i
        large_number = np.ceil(total_flows * large_ratio)
        #In the case there are not enough large or small flows using the ratio, we set thier number to 1
        if large_number == 0:
            large_number = 1
        small_number = total_flows - large_number
        if small_number == 0:
            small_number = 1
        perm_matrix = traffic_generator(large_number, small_number, large_load_ratio, net_curr.n, 0.01)
        temp_res = net_curr.test_four_algs(perm_matrix)
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


# net = NetworkEval(n=64, rd=0.01)
# net.bir = BirkDecomp()
# total_num = 585
# large_num_ratio = 0.2
# large_num = np.ceil(total_num * large_num_ratio)
# small_num = total_num - large_num
# perm_matrix = traffic_generator(large_num, small_num, 0.7, net.n, 0.01)
# res = net.test_four_algs(perm_matrix)
# print(res)
# #print(net_curr.test_four_algs(perm_matrix))
# bir = BirkDecomp()
# (p, al) = bir.birk_decomp(perm_matrix, 0.00001)
# print(p)
# al=np.array(al)
# print("endline")
# res = np.transpose(p)
# res2 = [np.transpose(np.mat(res * al).reshape(net_curr.n, net_curr.n)) for res, al, in zip(res, al)]
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
# zeros_mat = np.zeros((net_curr.n,net_curr.n))
#
# cumulative_sums = []
# for i in range(len(res2)):
#     zeros_mat+=res2[i]
#     cumulative_sums.append(zeros_mat.copy())
# print(cumulative_sums[0])
# print("endlin23fawfsde")
# cumlis =  [newM- ll for ll in cumulative_sums]
# print(res2[-1])
# #print(net_curr.pivot_alg_DCT(res2,al))
#
# print (net_curr.test_four_algs(perm_matrix))
