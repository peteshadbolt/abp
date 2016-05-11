from abp import GraphState
from abp import Client
import time

psi = Client()

psi.draw()
psi.add_nodes(range(10))
psi.draw()
psi.act_hadamard(0)
psi.act_hadamard(1)
psi.draw()
psi.act_cz(0, 1)
psi.draw()
psi.act_cz(0, 1)
server.draw()

server.shutdown()
