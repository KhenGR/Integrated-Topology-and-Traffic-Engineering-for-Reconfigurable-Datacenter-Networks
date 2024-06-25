from src.traficGen import *
from src.julia_birkDecomp import BirkDecomp


def power_range(start, stop, coff):
    """
    this gives a power given_range where each element is from
    {a,ca,c^2a,...,c^n*a}, where c^n*a<=b
    :param start: start of given_range
    :param stop: maximal element of given_range
    :param coff: factor
    :return: given_range of numbers
    """
    num_steps = int(np.floor(np.log(stop / start) / np.log(coff))) + 1
    # Generate the exponents
    exponents = np.arange(0, num_steps)
    # Generate the sequence using logspace
    result = start * np.power(coff, exponents)
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


def var_dist_line(arr) -> float:
    """
    #this function calculates the variation distance of one row of a matrix
    :arr the array to calculate
    """
    arr = np.array(arr)
    normalized_mat = arr / np.sum(arr)
    # This is always 1/len(arr) unless something is wrong
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
        :param rr: [sec] Round robin reconfiguration time
        :param rd: [sec] Demand aware reconfiguration time
        :param r: [bits/sec] transmission rate
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
        # Take maximal line sum
        row_sums = np.sum(m, axis=1)
        max_row_load = np.max(row_sums)
        # Take maximal element
        max_elem = np.max(m)
        constent_dct = (2 - (2 / self.n)) * (1 / self.r) * max_row_load
        max_elem_dct = (self.n - 1) * (1 / self.r) * max_elem
        return np.min((constent_dct, max_elem_dct))

    def pivot_alg_dct(self, p_lis, alpha):
        """
        this is the pivot alg form the paper.
        It finds the best pivot point for the composite system
        :param p_lis: a list of matchings
        :param alpha: a list of coefficients
        :return: results dict
        """
        sorted_alpha = np.array(sorted(alpha, reverse=True))
        sorted_p = sort_list_by_other_list(alpha, p_lis, rev=True)
        cumulative_dct_da = np.cumsum(sorted_alpha + self.rd)
        summarized_matrix = self.r * np.sum(sorted_p, axis=0)
        zeros_mat = np.zeros((self.n, self.n))
        cumulative_sums = []
        for i in range(len(sorted_p)):
            zeros_mat += self.r * sorted_p[i]
            cumulative_sums.append(zeros_mat.copy())
        cum_lis = [summarized_matrix - j for j in cumulative_sums]
        cumulative_dct_rr = [self.get_rr_dct(j) for j in cum_lis]
        all_pivot_results = [i + j for i, j, in zip(cumulative_dct_rr, cumulative_dct_da)]
        best_res_pivot = np.min(all_pivot_results)
        best_res_index = np.argmin(all_pivot_results)
        da_load = np.sum(sorted_alpha[0:best_res_index + 1])
        return {"best_res_pivot": best_res_pivot,
                "piv_index": (best_res_index, len(alpha) - best_res_index),
                "da_load": da_load}

    def test_three_systems(self, mat, birk_epsilon=0.00001):
        """
        Tests the DCT of our three systems, the demand aware, the round-robin
        and the composite system
        :param mat: The demand matrix
        :param birk_epsilon: the epsilon of the bvn decomposition
        :return:
        """
        (p, al) = self.bir.birk_decomp(mat, birk_epsilon)

        # The data which is the result of birk_decomp needs to be reshapen
        trans_p = np.transpose(p)
        total_arrs = [np.transpose(np.mat(transP * al).reshape(self.n, self.n)) for transP, al, in zip(trans_p, al)]
        # Get the pivot result
        pivot_dct_res_dict = self.pivot_alg_dct(total_arrs, al)
        pivot_dct = pivot_dct_res_dict["best_res_pivot"]
        index_piv_res = pivot_dct_res_dict["piv_index"]
        da_load = pivot_dct_res_dict["da_load"]
        # Send to the RR-sys the possibly slightly reduced matrix from the decomposition
        new_m = np.sum(total_arrs, axis=0)
        rr_dct = self.get_rr_dct(self.r * new_m)
        # Calculate the dct of DA system
        da_dct = np.sum(al) + len(al) * self.rd
        # Since we do not test the edge cases inside of the pivot_alg_dct function,
        # we test them here for the load
        if da_dct <= pivot_dct and da_dct <= rr_dct:
            da_load = 1
        elif rr_dct <= pivot_dct and rr_dct <= da_dct:
            da_load = 0
        return {"res": [da_dct, rr_dct, np.min((da_dct, rr_dct, pivot_dct))],
                "max": np.max(new_m), "var_dist": var_dist_mat(np.array(new_m)), "BvN_dist": len(al),
                "sparsity": sparsity_measure(np.array(new_m)), "piv_div_res": index_piv_res, "da_load": da_load}


def run_tests_flow_number(net_curr: NetworkEval, large_ratio, large_load_ratio, total_flows_range):
    """
    Tests a given_range of flows numbers as specified in total_flows_range
    :param net_curr: NetworkEval object
    :param large_ratio: ratio of large flows of total flows
    :param large_load_ratio: portion of the load of large flows
    :param total_flows_range: a list with a given_range of the number of models of flows to test
    :return: a dict with all of the results
    """
    res_list = []
    if net_curr.bir is None:
        net_curr.bir = BirkDecomp()
    for i in total_flows_range:
        total_flows = i
        large_number = np.ceil(np.ceil(total_flows) * large_ratio)
        # In the case there are not enough large or small flows using the ratio, we set thier number to 1
        # if large_number == 0:
        #     large_number = 1
        small_number = np.ceil(total_flows) - large_number
        if small_number == 0:
            small_number = 1
        perm_matrix = traffic_generator(large_number, small_number, large_load_ratio, net_curr.n, 0.01)
        temp_res = net_curr.test_three_systems(perm_matrix)
        res_list.append(temp_res.copy())
    return res_list


def run_tests_large_flow_load(net_curr, large_ratio, large_load_ratio_range, total_flows):
    """
    Tests a given_range of "large flow load" values as specified in large_load_ratio_range
    :param net_curr: NetworkEval object
    :param large_ratio: ratio of large flows of total flows
    :param large_load_ratio_range: a list with a given_range of the large flow load to test
    :param total_flows: total number of flows
    :return: a dict with all of the results
    """

    res_list = []
    if net_curr.bir is None:
        net_curr.bir = BirkDecomp()
    for i in large_load_ratio_range:
        large_load_ratio = i
        large_number = np.ceil(total_flows * large_ratio)
        # In the case there are not enough large or small flows using the ratio, we set thier number to 1
        if large_number == 0:
            large_number = 1
        small_number = total_flows - large_number
        if small_number == 0:
            small_number = 1
        perm_matrix = traffic_generator(large_number, small_number, large_load_ratio, net_curr.n, 0.01)
        temp_res = net_curr.test_three_systems(perm_matrix)
        res_list.append(temp_res.copy())
    return res_list


def run_tests_large_flow_ratio(net_curr, large_ratio_range, large_load_ratio, total_flows):
    """
    Tests a given range of "large ratio_range" values as specified in large_ratio_range
    :param net_curr: NetworkEval object
    :param large_ratio_range:  a list with a given_range of the number of large flow ratio  to test
    :param large_load_ratio: the ratio of the number of large flows
    :param total_flows: total number of flows
    :return: a dict with all of the results
    """

    res_list = []
    if net_curr.bir is None:
        net_curr.bir = BirkDecomp()
    for i in large_ratio_range:
        large_ratio = i
        large_number = np.ceil(total_flows * large_ratio)
        # In the case there are not enough large or small flows using the ratio, we set thier number to 1
        if large_number == 0:
            large_number = 1
        small_number = total_flows - large_number
        if small_number == 0:
            small_number = 1
        perm_matrix = traffic_generator(large_number, small_number, large_load_ratio, net_curr.n, 0.01)
        temp_res = net_curr.test_three_systems(perm_matrix)
        res_list.append(temp_res.copy())
    return res_list


