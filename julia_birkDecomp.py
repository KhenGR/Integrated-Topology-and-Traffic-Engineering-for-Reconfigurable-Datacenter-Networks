import juliacall
#One time run
##jl.seval("import Pkg")
##jl.seval("Pkg.add(\"BirkhoffDecomposition\")")
class birkDecomp:
    def __init__(self):
        self.jl = juliacall.newmodule("SomeName")
        self.jl.seval("using BirkhoffDecomposition")

    def birk_decomp(self, mat, epsilon=0.00000001):
        return self.jl.birkdecomp(mat, epsilon)


