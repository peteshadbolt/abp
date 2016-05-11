from abp.graphstate import GraphState
from abp.qi import CircuitModel
from abp import clifford
import numpy as np
import random
from tqdm import tqdm

REPEATS = 100

def test_single_qubit(n=1):
    """ A multi qubit test with Hadamards only"""
    for repeat in tqdm(range(REPEATS), desc="Testing against circuit model") :
        g = GraphState([0])
        c = CircuitModel(1)

        for i in range(100):
            op = random.randint(0, 23)
            g.act_local_rotation(0, op)
            c.act_local_rotation(0, clifford.unitaries[op])

        assert g.to_state_vector() == c


def test_hadamard_only_multiqubit(n=6):
    """ A multi qubit test with Hadamards only"""
    for repeat in tqdm(range(REPEATS), desc="Testing against circuit model") :
        g = GraphState(range(n))
        c = CircuitModel(n)

        for i in range(n):
            g.act_hadamard(i)
            c.act_hadamard(i)

        assert g.to_state_vector() == c

        for i in range(100):
            a, b = np.random.randint(0, n - 1, 2)
            if a != b:
                g.act_cz(a, b)
                c.act_cz(a, b)

        assert g.to_state_vector() == c


def test_all_multiqubit(n=4):
    """ A multi qubit test with arbitrary local rotations """
    g = GraphState(range(n))
    c = CircuitModel(n)
    for i in range(10):
        qubit = np.random.randint(0, n - 1)
        rotation = np.random.randint(0, 24 - 1)
        g.act_local_rotation(qubit, rotation)
        c.act_local_rotation(qubit, clifford.unitaries[rotation])

    assert g.to_state_vector() == c

    for repeat in tqdm(range(REPEATS), desc="Testing against circuit model") :
        a, b = np.random.randint(0, n-1, 2)
        if a != b:
            g.act_cz(a, b)
            c.act_cz(a, b)
            assert np.allclose(np.sum(np.abs(c.state)**2), 1)
            assert np.allclose(np.sum(np.abs(g.to_state_vector().state)**2), 1)

            if not g.to_state_vector() == c:
                print g
                print a, b
                print "Circuit:"
                print g.to_state_vector()
                print "Graph:"
                print c
                raise ValueError

    assert g.to_state_vector() == c
