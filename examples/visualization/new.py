from abp import GraphState, VizClient
from abp.util import xyz

v = VizClient()
g = GraphState(5)
for i in range(5):
    g.node[i]["position"] = xyz(i, 0, 0)
v.update(g)
