from abp import GraphState
from abp.util import xyz
from mock import simple_graph

def linear_cluster(n):
    g = GraphState(list(range(n)), vop="hadamard")
    g.act_circuit([(i, "hadamard") for i in range(n)])
    g.act_circuit([((i, i+1), "cz") for i in range(n-1)])
    return g 


def test_mercedes_example_1():
    """ Run an example provided by mercedes """
    g = linear_cluster(5)
    g.measure(3, "px")
    g.measure(2, "px")
    assert set(g.adj[0]) == {1}
    assert set(g.adj[1]) == {0, 4}
    assert set(g.adj[4]) == {1}


def test_single_qubit_measurements():
    """ Various simple tests of measurements """

    # Test that measuring |0> in Z gives 0
    g = GraphState([0], vop="hadamard")
    assert g.measure_z(0) == 0, "Measuring |0> in Z gives 0"

    # Test that measuring |1> in Z gives 1
    g = GraphState([0], vop="hadamard")
    g.act_local_rotation(0, "px")
    assert g.measure_z(0) == 1, "Measuring |1> in Z gives 1"

    # Test that measuring |+> in X gives 0
    g = GraphState([0], vop="hadamard")
    g.act_local_rotation(0, "hadamard")
    assert g.measure_x(0) == 0
    assert g.measure_x(0) == 0, "Measuring |+> in X gives 0"
    g.act_local_rotation(0, "pz")
    assert g.measure_x(0) == 1, "Measuring |-> in X gives 1"

    # Test something else
    assert g.measure_y(0, force=0) == 0

def test_is_determinate():
    """ Test whether asking if an outcome was random or determinate works """
    g = GraphState([0], vop="hadamard")
    assert g.measure_z(0, detail=True)["determinate"] == True
    assert g.measure_x(0, detail=True)["determinate"] == False


def test_copy():
    """ Make a copy of a graph """
    a = simple_graph()
    b = a.copy()
    assert a == b
    


