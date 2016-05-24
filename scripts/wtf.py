from abp import clifford, qi, GraphState
from anders_briegel import graphsim
import numpy as np
import itertools as it


""" This is an example of where we get a discrepancy """

def pete():
    a = GraphState(xrange(3))
    a.act_hadamard(0)
    a.act_hadamard(1)
    a.act_hadamard(2)
    a.act_cz(0, 1)
    a.act_cz(0, 2)
    a.act_local_rotation(0, 1)
    a.act_local_rotation(2, 3)
    a.act_cz(1,2)
    return a.adj_list()

def anders():
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

pete()

