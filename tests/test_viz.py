from graph import GraphState
import viz

def test_viz():
    g = GraphState()
    g.add_edge(0,1)
    g.add_edge(1,2)
    g.add_edge(2,0)
    g.add_edge(0,3)
    print g.vops
    viz.draw(g)
