import numpy as np
from abp import GraphState
from abp import qi
from anders_briegel import graphsim

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
    print g.to_state_vector()
    assert np.allclose(g.to_state_vector().state, qi.zero)

    g = GraphState([0])
    g.act_local_rotation(0, "hadamard")
    print g.to_state_vector()
    g.measure(0, "pz", 1)
    print g.to_state_vector()
    assert np.allclose(g.to_state_vector().state, qi.one)




def test_z_measurement_against_ab():
    for i in range(10):
        a = graphsim.GraphRegister(1)
        b = GraphState()
        b.add_node(0)
        #print a.measure(0, graphsim.lco_Z) 
        #print b.measure(0, "pz")
