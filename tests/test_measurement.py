from abp import GraphState
from anders_briegel import graphsim

def test_z_measurement():
    g = GraphState([0])
    assert g.measure_z(0, 0) == 0
    assert g.measure_z(0, 1) == 1


def test_z_measurement_against_ab():
    for i in range(10):
        a = graphsim.GraphRegister(1)
        b = GraphState()
        b.add_node(0)
        print a.measure(0, graphsim.lco_Z) 
        print b.measure(0, "pz")
