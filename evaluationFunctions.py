import numpy as np

from traficGen import *
from julia_birkDecomp import birkDecomp


class network_eval:
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
        return np.max((constent_DCT, max_elem_DCT))

    def pivot_alg_DCT(self,P_lis,alpha,epsilon):
        sort


    def test_four_algs(self, M, index, birk_epsilon, epsilon):
        bir = birkDecomp()
        (a, w) = bir.birk_decomp(M, birk_epsilon)
        totalArrs=a*w
        rotor_DCT = self.get_rotor_DCT(M)
        da_DCT = np.sum(w)+len(w)*self.rd


    return 1
