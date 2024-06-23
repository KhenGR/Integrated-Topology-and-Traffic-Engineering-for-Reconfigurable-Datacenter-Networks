import juliacall


def install_birkhoff_decomposition_pkg():
    """
    This will  (hopefully) install the julia pkg "BirkhoffDecomposition"
    This requires the installation of the juliacall lib
    Should be run only once.
    """

    # One time run
    jl = juliacall.newmodule("SomeName")
    jl.seval("import Pkg")
    jl.seval("Pkg.add(\"BirkhoffDecomposition\")")


class BirkDecomp:
    """
    This class is used to calculate the BVN decomposition using the julia lib "BirkhoffDecomposition"
    """

    def __init__(self):
        """
        Starts the juliacall module once
        """
        self.jl = juliacall.newmodule("SomeName")
        self.jl.seval("using BirkhoffDecomposition")

    def birk_decomp(self, mat, epsilon=0.00000001):
        """
        Wrapper for the BVN decomposition function call in the library
        :param mat: a double stochastic matrix
        :param epsilon: an epsilon parameter for the call
        :return: (list of matchings, list of coefficients)
        """
        return self.jl.birkdecomp(mat, epsilon)
