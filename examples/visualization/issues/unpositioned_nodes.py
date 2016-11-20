from abp import GraphState, VizClient
from abp.util import xyz

# Prepare to visualize
v = VizClient()

# Make a graph state with position attributes
g = GraphState()
for i in range(5):
    g.add_qubit(i, position=xyz(i, 0, 0), vop="identity")
g.act_czs((0,1),(1,2),(2,3),(3,4))

# Show it
v.update(g, 3)

# Add a qubit with no position
g.add_qubit('start')

# Show it
v.update(g)
