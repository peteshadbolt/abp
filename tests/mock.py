"""
Mock graphs used for testing
"""

import numpy as np
import abp
from abp import GraphState, clifford, qi
from numpy import random
import pytest

# We always run with A&B's CZ table when we are testing
clifford.use_old_cz()

class ABPWrapper(GraphState):

    """ A wrapper for abp, just to ensure determinism """

    def __init__(self, nodes=[]):
        abp.DETERMINISTIC = True
        super(ABPWrapper, self).__init__(nodes, vop="hadamard")

    def print_stabilizer(self):
        print(self.to_stabilizer())

    def __eq__(self, other):
        return self.to_json() == other.to_json()


class CircuitModelWrapper(qi.CircuitModel):

    def __init__(self, nodes=[]):
        assert list(nodes) == list(range(len(nodes)))
        super(CircuitModelWrapper, self).__init__(len(nodes))

    def act_circuit(self, circuit):
        """ Act a sequence of gates """
        for node, operation in circuit:
            if operation == "cz":
                self.act_cz(*node)
            else:
                u = clifford.unitaries[clifford.by_name[str(operation)]]
                self.act_local_rotation(node, u)


def random_pair(n):
    """ Helper function to get random pairs"""
    return tuple(random.choice(list(range(n)), 2, replace=False))


def random_graph_circuit(n=10, depth=100):
    """ A random Graph state. """
    return [(i, "hadamard") for i in range(n)] + \
           [(random_pair(n), "cz") for i in range(depth)]


def random_stabilizer_circuit(n=10, depth=100):
    """ Generate a random stabilizer state, without any VOPs """
    return random_graph_circuit(n, depth) + \
        [(i, random.choice(list(range(24)))) for i in range(n)]


def bell_pair():
    """ Generate a bell pair circuit """
    return [(0, "hadamard"), (1, "hadamard"), ((0, 1), "cz")]


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


def circuit_to_state(Base, n, circuit):
    """ Convert a circuit to a state, given a base class """
    g = Base(list(range(n)))
    g.act_circuit(circuit)
    return g



if __name__ == '__main__':
    for i in range(1000):
        test_circuit(random_graph_circuit(10), 10)
        test_circuit(random_stabilizer_circuit(10), 10)
