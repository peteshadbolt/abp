from abp.graphstate import GraphState
from anders_briegel import graphsim
import random
import difflib
import re

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


def test_2():
    N=10

    a = graphsim.GraphRegister(N)
    b = GraphState()

    for i in range(N):
        b.add_vertex(i)

    for i in range(100):
        if random.random()>0.5:
            j = random.randint(0, N-1)
            a.hadamard(j)
            b.act_hadamard(j)
        else:
            q = random.randint(0, N-2)
            a.cphase(q, q+1)
            b.act_cz(q, q+1)

    aa = a.get_adj_list()
    bb = b.adj_list()
    try:
        assert re.sub("\\s", "", aa) == re.sub("\\s", "", bb)
    except AssertionError:
        print aa
        print bb

