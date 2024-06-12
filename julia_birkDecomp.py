import juliacall
#One time run
##jl.seval("import Pkg")
##jl.seval("Pkg.add(\"BirkhoffDecomposition\")")
class birkDecomp:
    def __init__(self):
        self.jl = juliacall.newmodule("SomeName")
        self.jl.seval("using BirkhoffDecomposition")

    def birk_decomp(self, mat, epsilon=0.00001):
        return self.jl.birkdecomp(mat, epsilon)


# bir = birkDecomp()
# n = 5
# X = bir.jl.randomDoublyStochasticMatrix(n)
# #(a,w) = bir.jl.birkdecomp(X)
# (a, w) = bir.birk_decomp(X, 0.001)
# print(w)
# X  = bir.jl.randomDoublyStochasticMatrix(n)
# (a,w) = bir.jl.birkdecomp(X,0.001)
# print(w)
#jl.seval("import Pkg")
#jl.seval("Pkg.add(\"BirkhoffDecomposition\")")


# X  = jl.randomDoublyStochasticMatrix(n)
# print(X)
# # Compute exact decomposition
# (a,w) = jl.birkdecomp(X)
# print(w)
