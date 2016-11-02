from abp.fancy import GraphState
from abp.util import xyz
import itertools

psi = GraphState()
grid = itertools.product(range(10), range(10))
for i, (x, y) in enumerate(grid):
    psi.add_qubit(i, position=xyz(x, y, 0), vop=0)

for i in range(50):
    psi.act_cz(i, i+1)

psi.update()

