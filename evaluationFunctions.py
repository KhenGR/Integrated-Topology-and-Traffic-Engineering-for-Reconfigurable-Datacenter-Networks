import numpy as np

from traficGen import *
from julia_birkDecomp import birkDecomp


class network_eval:
    rd: float
    n: int
    r: float
    rr: float

    def __init__(self, n=64, rr=0, rd=0.015, r=10000000000):
        self.rd = rd
        self.n = n
        self.r = r
        self.rr = rr

    def get_rotor_DCT(self, M):
        #Take maximal line sum
        row_sums = np.sum(M, axis=1)
        max_row_load = np.max(row_sums)
        # Take maximal element
        max_elem = np.max(M)
        constent_DCT = (2 - 2 / self.n) * (1 / self.r) * max_row_load
        max_elem_DCT = (self.n - 1) * (1 / self.r) * max_elem
        return np.min((constent_DCT, max_elem_DCT))

    def pivot_alg_DCT(self,P_lis,alpha,epsilon):
        sorted_alpha = sorted(alpha, reverse=True)
        cumulative_sum = np.cumsum(sorted_alpha + self.rd)

    def test_four_algs(self, M, index=1, birk_epsilon=0.00001, epsilon=0.1):
        bir = birkDecomp()
        (a, w) = bir.birk_decomp(M, birk_epsilon)
        totalArrs=a*w
        rotor_DCT = self.get_rotor_DCT(self.r*M)
        da_DCT = np.sum(w)+len(w)*self.rd
        return (da_DCT,rotor_DCT)


perm_matrix = traffic_generator(2,3,0.95,64,0.01)
net = network_eval()
print(net.test_four_algs(perm_matrix))
