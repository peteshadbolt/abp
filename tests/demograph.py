from abp import GraphState

def demograph():
    """ A graph for testing with """
    g = GraphState([0,1,2,3,100,200])
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(0, 3)
    g.add_edge(100, 200)
    return g


