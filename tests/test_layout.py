from abp.graphstate import GraphState

def demograph():
    """ A graph for testing with """
    g = GraphState()
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(0, 3)
    g.add_edge(100, 200)
    return g


def test_nx_convert():
    g = demograph()
    n = g.to_networkx()
    assert len(g.ngbh) == len(n.edge)
    assert len(g.vops) == len(n.node)

def test_layout():
    g = demograph()
    g.layout()
    assert len(g.meta) == len(g.vops)
    assert "pos" in g.meta[0]
    assert "x" in g.meta[0]["pos"]

