from graph import GraphState
import tables as lc
import time


def demograph():
    g = GraphState()
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(0, 3)
    g.add_edge(100, 200)
    return g


def test_graph():
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
    assert g.vops[0] == lc.by_name["identity"]
    g.remove_vop(1, 1)
    assert g.vops[1] == lc.by_name["identity"]
    g.remove_vop(2, 1)
    assert g.vops[2] == lc.by_name["identity"]
    g.remove_vop(0, 1)
    assert g.vops[0] == lc.by_name["identity"]


def test_edgelist():
    """ Test making edgelists """
    g = demograph()
    el = g.edgelist()
    assert (0, 3) in el
    assert (0, 2) in el
    assert (100, 200) in el


def test_million_sites():
    """ Testing making really big graphs """
    g = GraphState()
    t = time.clock()
    for i in xrange(100000):
        g.add_edge(i, i + 1)
    print time.clock() - t
