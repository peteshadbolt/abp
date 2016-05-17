from abp import VisibleGraphState
import numpy as np

s = VisibleGraphState()
for i in range(200):
    x = 10*np.cos(np.pi*2*i/60)
    y = 10*np.sin(np.pi*2*i/60)
    s.add_node(i, {"position": (x, y, i/50.)})
    s.act_local_rotation(i, "hadamard")
for i in range(200-1):
    s.act_cz(i, i+1)
s.update()
