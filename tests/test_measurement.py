from abp import GraphState

def test_z_measurement():
    g = GraphState([0])
    assert g.measure_z(0, 0) == 0
    assert g.measure_z(0, 1) == 1




