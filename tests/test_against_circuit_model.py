from abp.graphstate import GraphState
from abp.qi import CircuitModel
from abp import clifford
import numpy as np
import random

def test_hadamard_only_multiqubit():
    """ A multi qubit test with Hadamards only"""
    n = 4
    g = GraphState(range(n))
    c = CircuitModel(n)

    for i in range(n):
        g.act_hadamard(i)
        c.act_hadamard(i)

    assert g.to_state_vector() == c

    for i in range(100):
        a, b = np.random.randint(0, n-1, 2)
        if a != b:
            g.act_cz(a, b)
            c.act_cz(a, b)

    assert g.to_state_vector() == c


def test_all_multiqubit():
    """ A multi qubit test with arbitrary local rotations """
    n = 4
    g = GraphState(range(n))
    c = CircuitModel(n)

    for i in range(10):
        qubit = np.random.randint(0, n-1)
        rotation = np.random.randint(0, 24-1)
        g.act_local_rotation(qubit, rotation)
        c.act_local_rotation(qubit, clifford.unitaries[rotation])


    assert g.to_state_vector() == c

    #for i in range(100):
        #a, b = np.random.randint(0, n-1, 2)
        #if a != b:
            #g.act_cz(a, b)
            #c.act_cz(a, b)

    assert g.to_state_vector() == c

