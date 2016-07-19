from abp import GraphState
from anders_briegel import graphsim

def test_measurements():
    g = GraphState([0])
    print g
    assert all(g.measure(0, "pz") == 0 for i in range(100)), "Measuring |0> in Z gives 0"


def test_z_measurement_against_ab():
    for i in range(10):
        a = graphsim.GraphRegister(1)
        b = GraphState()
        b.add_node(0)
        #print a.measure(0, graphsim.lco_Z) 
        #print b.measure(0, "pz")
