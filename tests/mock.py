"""
Mock graphs used for testing
"""

import numpy as np
from abp import GraphState, clifford
from anders_briegel import graphsim
from numpy import random

# We always run with A&B's CZ table when we are testing
clifford.use_old_cz()


class AndersWrapper(graphsim.GraphRegister):

    """ A wrapper for A&B to make the interface identical and enable equality testing """

    def __init__(self, nodes):
        assert list(nodes) == range(len(nodes))
        super(AndersWrapper, self).__init__(len(nodes))

    def act_local_rotation(self, qubit, operation):
        operation = clifford.by_name[str(operation)]
        op = graphsim.LocCliffOp(operation)
        super(AndersWrapper, self).local_op(qubit, op)

    def act_cz(self, a, b):
        super(AndersWrapper, self).cphase(a, b)

    def measure(self, qubit, basis, force):
        basis = clifford.by_name[basis]
        basis = {1: graphsim.lco_X,
                 2: graphsim.lco_Y,
                 3: graphsim.lco_Z}[clifford.by_name[basis]]
        super(AndersWrapper, self).measure(qubit, basis, None, force)

    def __eq__(self, other):
        return self.to_json() == other.to_json()

    def act_circuit(self, circuit):
        for node, operation in circuit:
            if operation == "cz":
                self.act_cz(*node)
            else:
                self.act_local_rotation(node, operation)


class ABPWrapper(GraphState):

    """ A wrapper for abp, just to ensure determinism """

    def __init__(self, nodes=[]):
        super(ABPWrapper, self).__init__(nodes, deterministic=True)


def random_pair(n):
    """ Helper function to get random pairs"""
    return tuple(random.choice(range(n), 2, replace=False))


def random_graph_state(n=10):
    """ A random Graph state. """
    czs = [(random_pair(n), "cz") for i in range(n * 2)]
    for Base in AndersWrapper, ABPWrapper:
        g = Base(range(n))
        g.act_circuit((i, "hadamard") for i in range(n))
        g.act_circuit(czs)
        yield g


def random_stabilizer_state(n=10):
    """ Generate a random stabilizer state, without any VOPs """
    rotations = [(i, random.choice(range(24))) for i in range(n)]
    for g in random_graph_state():
        g.act_circuit(rotations)
        yield g


def bell_pair():
    for Base in AndersWrapper, ABPWrapper:
        g = Base((0, 1))
        g.act_circuit(((0, "hadamard"), (1, "hadamard"), ((0, 1), "cz")))
        yield g


def onequbit():
    for Base in AndersWrapper, ABPWrapper:
        g = Base((0,))
        yield g


def named_node_graph():
    """ A graph with named nodes"""
    edges = (0, 1), (1, 2), (2, 0), (0, 3), (100, 200), (200, "named")
    g = ABPWrapper([0, 1, 2, 3, 100, 200, "named"])
    g.act_circuit((i, "hadamard") for i in g.node)
    g.act_circuit((edge, "cz") for edge in edges)
    return g


def simple_graph():
    """ A simple graph to test with"""
    edges = (0, 1), (1, 2), (2, 0), (0, 3), (100, 200)
    g = ABPWrapper([0, 1, 2, 3, 100, 200])
    g.act_circuit((i, "hadamard") for i in g.node)
    g.act_circuit((edge, "cz") for edge in edges)
    return g


if __name__ == '__main__':
    a, b = random_graph_state()
    assert a == b

    a, b = random_stabilizer_state()
    assert a == b

    print named_node_graph()
