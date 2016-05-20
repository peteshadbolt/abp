from abp import GraphState

N = int(1e6)
g = GraphState()
g.add_nodes(xrange(N))

for i in range(N):
    g.act_hadamard(i)

for i in range(N):
    g.act_cz(i, (i+1) % N)

