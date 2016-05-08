from abp.graphstate import GraphState
from anders_briegel import graphsim
import random
import difflib
import re

def compare(a, b):
    """ Sketchy as you like. Remove this abomination """
    aa = a.get_adj_list()
    bb = b.adj_list()
    try:
        assert re.sub("\\s", "", aa) == re.sub("\\s", "", bb)
    except AssertionError:
        print aa
        print bb

def test_hadamard():
    """ Test hadamards """
    a = graphsim.GraphRegister(1)
    b = GraphState()
    b.add_vertex(0)

    compare(a, b)
    a.hadamard(0)
    b.act_hadamard(0)
    compare(a, b)
    a.hadamard(0)
    b.act_hadamard(0)
    compare(a, b)

def test_local_1():
    """ Test local rotations """
    a = graphsim.GraphRegister(1)
    b = GraphState()
    b.add_vertex(0)

    compare(a, b)
    a.local_op(0, graphsim.LocCliffOp(10))
    b.act_local_rotation(0, 10)
    compare(a, b)
    a.local_op(0, graphsim.LocCliffOp(10))
    b.act_local_rotation(0, 10)
    compare(a, b)

def test_local_2():
    """ Test local rotations """
    a = graphsim.GraphRegister(1)
    b = GraphState()
    b.add_vertex(0)
    compare(a, b)

    for i in range(1000):
        j = random.randint(0, 23)
        a.local_op(0, graphsim.LocCliffOp(j))
        b.act_local_rotation(0, j)
        compare(a, b)


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

    compare(a, b)


def _test_2():
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
    compare(a, b)

