from abp.graphstate import GraphState
from abp import clifford
import time


def demograph():
    """ A graph for testing with """
    g = GraphState()
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(0, 3)
    g.add_edge(100, 200)
    return g


def test_graph_basic():
    """ Test that we can construct graphs, delete edges, whatever """
    g = demograph()
    assert g.ngbh[0] == set([1, 2, 3])
    g.del_edge(0, 1)
    assert g.ngbh[0] == set([2, 3])
    assert g.has_edge(1, 2)
    assert not g.has_edge(0, 1)


def test_local_complementation():
    """ Test that local complementation works as expected """
    g = demograph()
    g.local_complementation(0)
    assert g.has_edge(0, 1)
    assert g.has_edge(0, 2)
    assert not g.has_edge(1, 2)
    assert g.has_edge(3, 2)
    assert g.has_edge(3, 1)

    # TODO: test VOP conditions


def test_remove_vop():
    """ Test that removing VOPs really works """
    g = demograph()
    g.remove_vop(0, 1)
    assert g.vops[0] == clifford.by_name["identity"]
    g.remove_vop(1, 1)
    assert g.vops[1] == clifford.by_name["identity"]
    g.remove_vop(2, 1)
    assert g.vops[2] == clifford.by_name["identity"]
    g.remove_vop(0, 1)
    assert g.vops[0] == clifford.by_name["identity"]


def test_edgelist():
    """ Test making edgelists """
    g = demograph()
    el = g.edgelist()
    assert (0, 3) in el
    assert (0, 2) in el
    assert (100, 200) in el


def test_stress():
    """ Testing that making a graph of ten thousand qubits takes less than half a second"""
    g = GraphState()
    t = time.clock()
    for i in xrange(100000):
        g.add_edge(i, i + 1)
    assert time.clock() - t < .5


def test_cz():
    """ Test CZ gate """
    g = GraphState()
    g.add_vertex(0)
    g.add_vertex(1)
    g.act_local_rotation(0, clifford.by_name["hadamard"])
    g.act_local_rotation(1, clifford.by_name["hadamard"])
    g.act_local_rotation(1, clifford.by_name["py"])
    assert not g.has_edge(0, 1)
    g.act_cz(0, 1)
    assert g.has_edge(0, 1)

def test_stabilizer():
    """ Test that we can generate stabilizers okay """
    g = demograph()
    stab = g.to_stabilizer()
    #TODO: sux
    #assert len(stab.split("\n")) == g.order()

