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
