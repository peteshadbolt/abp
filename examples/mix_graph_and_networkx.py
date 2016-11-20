from abp import NXGraphState
from abp.util import xyz
import networkx as nx

n = 10
g = NXGraphState(range(n))
nx.set_node_attributes(g, "color", "red")
g.add_edges_from([i, i+1] for i in range(n-1))
print g.node[0]["color"]

