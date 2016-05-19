from demograph import demograph

#TODO

def _test_nx_convert():
    g = demograph()
    n = g.to_networkx()
    assert len(g.ngbh) == len(n.edge)
    assert len(g.vops) == len(n.node)

def _test_layout():
    g = demograph()
    g.layout()
    assert len(g.meta) == len(g.vops)
    assert "pos" in g.meta[0]
    assert "x" in g.meta[0]["pos"]

