from __future__ import absolute_import
from __future__ import print_function
from abp import GraphState

edges = (0, 1), (1, 2), (2, 0), (0, 3), (100, 200)
g = GraphState([0, 1, 2, 3, 100, 200])
g.act_circuit((i, "hadamard") for i in g.node)
g.act_circuit((edge, "cz") for edge in edges)

g.act_local_rotation(3, 9)

print(g.to_stabilizer())

