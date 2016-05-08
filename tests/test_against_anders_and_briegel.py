from abp.graphstate import GraphState
from anders_briegel import graphsim

def test_1():
    N=10

    a = graphsim.GraphRegister(N)
    b = GraphState()

    for i in range(N):
        a.hadamard(i)
        b.add_vertex(i)
        b.act_hadamard(i)

    for i in range(N-1):
        a.cphase(i, i+1)
        b.act_cz(i, i+1)

    assert a.get_adj_list() == b.adj_list()
