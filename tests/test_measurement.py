from abp import GraphState
from anders_briegel import graphsim

def test_measurements():

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

    # Test random outcomes
    ones = 0
    for i in range(1000):
        g = GraphState([0])
        g.act_local_rotation(0, "hadamard")
        ones += g.measure(0, "pz")
    assert 400 < ones < 600, "This is a probabilistic test!"



def test_z_measurement_against_ab():
    for i in range(10):
        a = graphsim.GraphRegister(1)
        b = GraphState()
        b.add_node(0)
        #print a.measure(0, graphsim.lco_Z) 
        #print b.measure(0, "pz")
