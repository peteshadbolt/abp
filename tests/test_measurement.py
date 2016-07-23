import numpy as np
from abp import GraphState
from abp import qi, clifford
from anders_briegel import graphsim
from tqdm import tqdm
import random

REPEATS = 100000
LOCAL_ROTATION = 0
CZ = 1
MEASURE = 2

def test_single_qubit_measurements():
    """ Various simple tests of measurements """

    # Test that measuring |0> in Z gives 0
    g = GraphState([0])
    assert g.measure(0, "pz") == 0, "Measuring |0> in Z gives 0"

    # Test that measuring |1> in Z gives 1
    g = GraphState([0])
    g.act_local_rotation(0, "px")
    assert g.measure(0, "pz") == 1, "Measuring |1> in Z gives 1"

    # Test that measuring |+> in X gives 0
    g = GraphState([0])
    g.act_local_rotation(0, "hadamard")
    assert g.measure(0, "px") == 0
    assert g.measure(0, "px") == 0, "Measuring |+> in X gives 0"
    g.act_local_rotation(0, "pz")
    assert g.measure(0, "px") == 1, "Measuring |-> in X gives 1"

def test_random_outcomes():
    """ Testing random behaviour """
    ones = 0
    for i in range(1000):
        g = GraphState([0])
        g.act_local_rotation(0, "hadamard")
        ones += g.measure(0, "pz")
    assert 400 < ones < 600, "This is a probabilistic test!"

def test_projection():
    """ Test that projection works correctly """
    g = GraphState([0])
    g.act_local_rotation(0, "hadamard")
    g.measure(0, "pz", 0)
    assert np.allclose(g.to_state_vector().state, qi.zero)

def test_another_projection():
    """ This one fails at the moment """
    g = GraphState([0])
    g.act_local_rotation(0, "hadamard")
    g.measure(0, "pz", 1)
    assert np.allclose(g.to_state_vector().state, qi.one)


