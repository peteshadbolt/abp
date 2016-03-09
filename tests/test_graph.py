from graph import Graph

def test_graph():
    g = Graph(3)
    g.add_edge(0,1)
    g.add_edge(1,2)
    g.add_edge(2,0)
    assert g.neighbours[0]==set([1,2])

    g.del_edge(0,1)
    assert g.neighbours[0]==set([2])
    el = g.edgelist()
    assert (1,2) in el
    assert not (0,1) in el
    assert len(el)==2

    assert g.has_edge(1,2)
    assert not g.has_edge(0,1)
