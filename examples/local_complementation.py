from abp.fancy import GraphState
from abp.util import xyz
from abp.clifford import *

psi = GraphState()
psi.add_node(0, position = xyz(0, 0))
psi.add_node(1, position = xyz(1, 1))
psi.add_node(2, position = xyz(3, 2))
psi.add_node(3, position = xyz(0, 3))

for n in psi.node:
    psi.act_hadamard(n)

psi.act_cz(0, 1)
psi.act_cz(0, 3)
psi.act_cz(1, 3)
psi.act_cz(1, 2)
while True:
    psi.update()
    psi.local_complementation(1)
