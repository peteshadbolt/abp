"""
Mock graphs used for testing
"""

import numpy as np
import abp
from abp import GraphState, clifford, qi
from numpy import random
import pytest
from anders_briegel import graphsim

# We always run with A&B's CZ table when we are testing
clifford.use_old_cz()


class AndersWrapper(graphsim.GraphRegister):

    """ A wrapper for A&B to make the interface identical and enable equality testing """

    def __init__(self, nodes):
        assert list(nodes) == list(range(len(nodes)))
        super(AndersWrapper, self).__init__(len(nodes))

    def act_local_rotation(self, qubit, operation):
        operation = clifford.by_name[str(operation)]
        op = graphsim.LocCliffOp(operation)
        super(AndersWrapper, self).local_op(qubit, op)

    def act_cz(self, a, b):
        super(AndersWrapper, self).cphase(a, b)

    def measure(self, qubit, basis, force):
        basis = {1: graphsim.lco_X,
                 2: graphsim.lco_Y,
                 3: graphsim.lco_Z}[clifford.by_name[str(basis)]]
        return super(AndersWrapper, self).measure(qubit, basis, None, force)

    def __eq__(self, other):
        return self.to_json() == other.to_json()

    def act_circuit(self, circuit):
        for operation, node in circuit:
            if operation == "cz":
                self.act_cz(*node)
            else:
                self.act_local_rotation(node, operation)


def test_circuit(circuit, n):
    """ Check that two classes exhibit the same behaviour for a given circuit """
    a = circuit_to_state(ABPWrapper, n, circuit)
    b = circuit_to_state(AndersWrapper, n, circuit)
    assert a == b

