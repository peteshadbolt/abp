import numpy as np
from abp import GraphState
from abp import qi, clifford
from tqdm import tqdm
import random
import itertools as it


def test_single_qubit_measurements():
    """ Various simple tests of measurements """

    # Test that measuring |0> in Z gives 0
    g = GraphState([0], vop="hadamard")
    assert g.measure(0, "pz") == 0, "Measuring |0> in Z gives 0"

    # Test that measuring |1> in Z gives 1
    g = GraphState([0], vop="hadamard")
    g.act_local_rotation(0, "px")
    assert g.measure(0, "pz") == 1, "Measuring |1> in Z gives 1"

    # Test that measuring |+> in X gives 0
    g = GraphState([0], vop="hadamard")
    g.act_local_rotation(0, "hadamard")
    assert g.measure(0, "px") == 0
    assert g.measure(0, "px") == 0, "Measuring |+> in X gives 0"
    g.act_local_rotation(0, "pz")
    assert g.measure(0, "px") == 1, "Measuring |-> in X gives 1"


def test_type():
    """ Test that the output is always an int """
    for r, m, f in it.product(range(24), ("px", "py", "pz"), (0, 1)):
        g = GraphState([0], vop="hadamard")
        g.act_local_rotation(0, r)
        assert str(g.measure(0, m)) in "01"
        assert str(g.measure(0, m, f)) in "01"
        assert g.measure(0, m, f, detail=True)["determinate"] == True


def test_random_outcomes():
    """ Testing random behaviour """
    ones = 0
    for i in range(1000):
        g = GraphState([0], vop="hadamard")
        g.act_local_rotation(0, "hadamard")
        ones += g.measure(0, "pz")
    assert 400 < ones < 600, "This is a probabilistic test!"


def test_projection():
    """ Test that projection works correctly """
    g = GraphState([0], vop="hadamard")
    g.act_local_rotation(0, "hadamard")
    g.measure(0, "pz", 0)
    assert np.allclose(g.to_state_vector().state, qi.zero)

    # Now project onto |1>
    g = GraphState([0], vop="hadamard")
    g.act_local_rotation(0, "hadamard")
    g.measure(0, "pz", 1)
    assert np.allclose(g.to_state_vector().state, qi.one)

def test_measure_sequence():
    """ Simple test of measurement sequences """
    g = GraphState(2, vop="identity")
    g.act_cz(0, 1)
    assert g.measure_sequence(((0, "px"), (1, "px")), forces=(0, 1)) == [0, 1]
    assert len(g.edgelist()) == 0
    assert g.node[1]["vop"] == clifford.pz


