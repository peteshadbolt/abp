from abp.graphstate import GraphState
from abp.util import xyz
import networkx as nx

def simple_test():
    g = GraphState()
    g.add_node(0, position = xyz(10, 0, 0))
    g.add_node(1, position = xyz(1, 0, 0))
    g.act_hadamard(0)
    g.act_hadamard(1)
    g.act_cz(0, 1)
    print g.node[0]["position"]
    print nx.to_edgelist(g)

