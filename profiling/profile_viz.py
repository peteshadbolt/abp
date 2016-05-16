from abp import VisibleGraphState

s = VisibleGraphState()
for i in range(1000):
    s.add_node(i)
    s.act_local_rotation(i, "hadamard")
s.update()
for i in range(1000-1):
    s.act_cz(i, i+1)
s.update()
