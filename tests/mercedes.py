from abp import GraphState
from abp.util import xyz

def linear_cluster(n):
    g = GraphState(range(n))
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


