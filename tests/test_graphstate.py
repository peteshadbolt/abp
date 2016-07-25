from abp import GraphState
from abp import clifford
from mock import simple_graph
import time


def test_graph_basic():
    """ Test that we can construct graphs, delete edges, whatever """
    g = simple_graph()
    assert set(g.adj[0].keys()) == set([1, 2, 3])
    g._del_edge(0, 1)
    assert set(g.adj[0].keys()) == set([2, 3])
    assert g.has_edge(1, 2)
    assert not g.has_edge(0, 1)


def test_local_complementation():
    """ Test that local complementation works as expected """
    g = simple_graph()
    g.local_complementation(0)
    assert g.has_edge(0, 1)
    assert g.has_edge(0, 2)
    assert not g.has_edge(1, 2)
    assert g.has_edge(3, 2)
    assert g.has_edge(3, 1)

    # TODO: test VOP conditions


def test_remove_vop():
    """ Test that removing VOPs really works """
    g = simple_graph()
    g.remove_vop(0, 1)
    assert g.node[0]["vop"] == clifford.by_name["identity"]
    g.remove_vop(1, 1)
    assert g.node[1]["vop"] == clifford.by_name["identity"]
    g.remove_vop(2, 1)
    assert g.node[2]["vop"] == clifford.by_name["identity"]
    g.remove_vop(0, 1)
    assert g.node[0]["vop"] == clifford.by_name["identity"]


def test_edgelist():
    """ Test making edgelists """
    g = simple_graph()
    el = g.edgelist()
    assert (0, 3) in el
    assert (0, 2) in el
    assert (100, 200) in el


def test_stress(n = int(1e5)):
    """ Testing that making a graph of ten thousand qubits takes less than half a second"""
    g = GraphState(range(n+1))
    t = time.clock()
    for i in xrange(n):
        g._add_edge(i, i + 1)
    assert time.clock() - t < .5


def test_cz():
    """ Test CZ gate """
    g = GraphState([0, 1])
    g.act_local_rotation(0, clifford.by_name["hadamard"])
    g.act_local_rotation(1, clifford.by_name["hadamard"])
    g.act_local_rotation(1, clifford.by_name["py"])
    assert not g.has_edge(0, 1)
    g.act_cz(0, 1)
    assert g.has_edge(0, 1)

def test_stabilizer():
    """ Test that we can generate stabilizers okay """
    g = simple_graph()
    stab = g.to_stabilizer()
    #TODO

