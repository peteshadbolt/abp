"""
Mock graphs used for testing
"""

import numpy as np
from abp import GraphState, clifford
from anders_briegel import graphsim

# We always run with A&B's CZ table when we are testing
clifford.use_old_cz()


class AndersWrapper(graphsim.GraphRegister):

    """ A wrapper for A&B to make the interface identical and enable equality testing """

    def __init__(self, nodes):
        assert list(nodes) == range(len(nodes))
        super(AndersWrapper, self).__init__(len(nodes))

    def act_local_rotation(qubit, operation):
        super(AndersWrapper, self).local_op(
            qubit, graphsim.LocCliffOp(operation))

    def act_cz(a, b):
        super(AndersWrapper, self).cphase(a, b)

    def measure(qubit, basis, force):
        basis = clifford.by_name[basis]
        basis = {1: graphsim.lco_X, 
                 2: graphsim.lco_Y, 
                 3: graphsim.lco_Z}[clifford.by_name[basis]]
        super(AndersWrapper, self).measure(qubit, basis, None, force)

    def __str__(self):
        return "A wrapped A&B state ({})".format(super(AndersWrapper, self).__str__())

    def __repr__(self):
        return self.__str__()

class PeteWrapper(GraphState):

    """ A wrapper for abp, just to ensure determinism """

def random_graph_state(N=10):
    """ A random Graph state. """

    for base in PeteWrapper, AndersWrapper:
        g = base(range(N))

        for i in range(N):
            g.act_hadamard(i)

        for i in range(10):
            j, k = np.random.choice(range(N), 2, replace=False)
            g.act_cz(j, k)

        yield g


def random_stabilizer_state(N=10):
    a, b = random_state()

    for i in range(N):
        j = np.random.choice(range(N))
        k = np.random.choice(range(24))
        a.act_local_rotation(j, k)
        b.local_op(j, graphsim.LocCliffOp(k))

    return a, b


def bell():
    a = GraphState(range(2))
    b = graphsim.GraphRegister(2)
    a.act_hadamard(0)
    a.act_hadamard(1)
    b.hadamard(0)
    b.hadamard(1)
    a.act_cz(0, 1)
    b.cphase(0, 1)
    return a, b


def onequbit():
    a = GraphState(range(1))
    b = graphsim.GraphRegister(1)
    return a, b


def demograph():
    """ A graph for testing with """
    g = GraphState([0, 1, 2, 3, 100, 200])
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(0, 3)
    g.add_edge(100, 200)
    return g
