from abp.graph import GraphState
from abp import viz


def test_viz():
    g = GraphState()
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(0, 3)
    g.add_edge(100, 200)
    # g.remove_vop(0, 1)
    viz.draw(g)
