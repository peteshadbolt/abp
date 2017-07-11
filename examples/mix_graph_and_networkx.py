from __future__ import absolute_import
from __future__ import print_function
from abp import NXGraphState
from abp.util import xyz
import networkx as nx
from six.moves import range

n = 10
g = NXGraphState(list(range(n)))
nx.set_node_attributes(g, "color", "red")
g.add_edges_from([i, i+1] for i in range(n-1))
print(g.node[0]["color"])

