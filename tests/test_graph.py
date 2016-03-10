from graph import *

def test_graph():
    g, v = graph()
    add_edge(g, 0,1)
    add_edge(g, 1,2)
    add_edge(g, 2,0)
    assert g[0]==set([1,2])

    del_edge(g, 0,1)
    assert g[0]==set([2])
    el = edgelist(g)
    assert (1,2) in el
    assert not (0,1) in el
    assert len(el)==2

    assert has_edge(g, 1,2)
    assert not has_edge(g, 0,1)

def test_local_complementation():
    """ Test that local complementation works as expected """
    g, vops = graph()
    add_edge(g, 0, 1)
    add_edge(g, 0, 2)
    add_edge(g, 1, 2)
    add_edge(g, 0, 3)
    local_complementation(g, vops, 0)
    assert has_edge(g, 0, 1)
    assert has_edge(g, 0, 2)
    assert not has_edge(g, 1, 2)
    assert has_edge(g, 3, 2)
    assert has_edge(g, 3, 1)

    # TODO: test VOP conditions

def test_remove_vop():
    """ Test that removing VOPs really works """
    g, vops = graph()
    add_edge(g, 0, 1)
    add_edge(g, 0, 2)
    add_edge(g, 1, 2)
    add_edge(g, 0, 3)
    remove_vop(g, vops, 0, 1)
    assert vops[0] == clifford.by_name["identity"]
    remove_vop(g, vops, 1, 1)
    assert vops[1] == clifford.by_name["identity"]
    remove_vop(g, vops, 2, 1)
    assert vops[2] == clifford.by_name["identity"]
    remove_vop(g, vops, 0, 1)
    assert vops[0] == clifford.by_name["identity"]

