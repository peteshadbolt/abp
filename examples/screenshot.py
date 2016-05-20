from abp.fancy import GraphState
from abp.util import xyz
import numpy as np

N = 100
g = GraphState()
for i in range(N):
    theta = 2*np.pi*i/30
    pos = xyz(5*np.cos(theta), 5*np.sin(theta), i/10.)
    g.add_node(i, position = pos, vop=0)

for i in range(N):
    g.act_cz(i, (i+1) % N)
    g.act_local_rotation(i, 12)
    g.act_local_rotation(i, 10)

