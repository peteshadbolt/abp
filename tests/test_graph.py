from graph import GraphState
import tables as lc

def test_graph():
    g = GraphState()
    g.add_edge(0,1)
    g.add_edge(1,2)
    g.add_edge(2,0)
    assert g.ngbh[0]==set([1,2])

    g.del_edge(0,1)
    assert g.ngbh[0]==set([2])
    el = g.edgelist()
    assert (1,2) in el
    assert not (0,1) in el
    assert len(el)==2

    assert g.has_edge(1,2)
    assert not g.has_edge(0,1)

def test_local_complementation():
    """ Test that local complementation works as expected """
    g = GraphState()
    g.add_edge(0,1)
    g.add_edge(1,2)
    g.add_edge(2,0)
    g.add_edge(0,3)
    g.local_complementation(0)
    assert g.has_edge(0, 1)
    assert g.has_edge(0, 2)
    assert not g.has_edge(1, 2)
    assert g.has_edge(3, 2)
    assert g.has_edge(3, 1)

    # TODO: test VOP conditions

def test_remove_vop():
    """ Test that removing VOPs really works """
    g = GraphState()
    g.add_edge(0,1)
    g.add_edge(1,2)
    g.add_edge(2,0)
    g.add_edge(0,3)
    g.remove_vop(0, 1)
    assert g.vops[0] == lc.by_name["identity"]
    g.remove_vop(1, 1)
    assert g.vops[1] == lc.by_name["identity"]
    g.remove_vop(2, 1)
    assert g.vops[2] == lc.by_name["identity"]
    g.remove_vop(0, 1)
    assert g.vops[0] == lc.by_name["identity"]

