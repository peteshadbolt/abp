from abp import clifford, qi, GraphState
from anders_briegel import graphsim
import numpy as np
import itertools as it

a = GraphState()
a.node = {0: {'vop': 1}, 1: {'vop': 0}, 2: {'vop': 3}}
a.adj = {0: {1: {}, 2: {}}, 1: {0: {}}, 2: {0: {}}}

a.act_cz(1,2)
print a.adj_list()



b = graphsim.GraphRegister(3)
b.hadamard(0)
b.hadamard(1)
b.hadamard(2)
b.cphase(0, 1)
b.cphase(0, 2)
b.local_op(0, graphsim.LocCliffOp(1))
b.local_op(2, graphsim.LocCliffOp(3))

b.cphase(1,2)
b.print_adj_list()
