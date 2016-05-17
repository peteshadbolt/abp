from abp.viz import VisibleGraphState
import numpy as np

s = VisibleGraphState()
for i in range(200):
    x = 10*np.cos(np.pi*2*i/60)
    y = 10*np.sin(np.pi*2*i/60)
    s.add_node(i, {"position": (round(x, 2), round(y, 2), round(i/50., 2))})
    s.act_local_rotation(i, "hadamard")
for i in range(200-1):
    s.act_cz(i, i+1)

