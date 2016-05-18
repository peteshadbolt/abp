from abp.viz import VisibleGraphState
import numpy as np
import time

s = VisibleGraphState()
for i in range(200):
    x = 10*np.cos(np.pi*2*i/60)
    y = 10*np.sin(np.pi*2*i/60)
    s.add_node(i, {"position": {"x":round(x, 2), "y":round(y, 2), "z":round(i/50., 2)}})
    s.act_local_rotation(i, "hadamard")
for i in range(200-1):
    s.act_cz(i, i+1)
    time.sleep(.3)
    s.update()

