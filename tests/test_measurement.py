from abp import GraphState

def test_z_measurement():
    g = GraphState(0)
    assert g.measure_z(0, 0) == 0
    assert g.measure_z(0, 1) == 1
    assert not all(g.measure_z(0) == 0 for i in range(100))

    g.act_hadamard(0)
    print g
    assert all(g.measure_z(0) == 1 for i in range(100))



