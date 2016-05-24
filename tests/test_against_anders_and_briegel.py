from abp import GraphState
from anders_briegel import graphsim
from abp import CircuitModel
from abp import clifford
import random
import difflib
import re
from copy import deepcopy

def compare(a, b):
    """ TODO: Sketchy as you like. Remove this abomination """
    aa = a.get_adj_list()
    bb = b.adj_list()
    try:
        assert re.sub("\\s", "", aa) == re.sub("\\s", "", bb)
    except AssertionError:
        print aa
        print bb
        raise

def isequal(a, b):
    """ TODO: Sketchy as you like. Remove this abomination """
    aa = a.get_adj_list()
    bb = b.adj_list()
    return re.sub("\\s", "", aa) == re.sub("\\s", "", bb)


def test_hadamard():
    """ Test hadamards """
    a = graphsim.GraphRegister(1)
    b = GraphState()
    b.add_node(0)

    compare(a, b)
    a.hadamard(0)
    b.act_hadamard(0)
    compare(a, b)
    a.hadamard(0)
    b.act_hadamard(0)
    compare(a, b)


def test_local_rotations():
    """ Test local rotations """
    a = graphsim.GraphRegister(1)
    b = GraphState()
    b.add_node(0)
    compare(a, b)

    for i in range(1000):
        j = random.randint(0, 23)
        a.local_op(0, graphsim.LocCliffOp(j))
        b.act_local_rotation(0, j)
        compare(a, b)


def test_cz_table(N=10):
    """ Test the CZ table """

    clifford.use_old_cz()

    for i in range(24):
        for j in range(24):

            a = graphsim.GraphRegister(2)
            b = GraphState()
            b.add_nodes([0, 1])

            a.local_op(0, graphsim.LocCliffOp(i))
            b.act_local_rotation(0, i)
            a.local_op(1, graphsim.LocCliffOp(j))
            b.act_local_rotation(1, j)

            a.cphase(0, 1)
            b.act_cz(0, 1)

            compare(a, b)

    for i in range(24):
        for j in range(24):

            a = graphsim.GraphRegister(2)
            b = GraphState()
            b.add_nodes([0, 1])

            a.local_op(0, graphsim.LocCliffOp(10))
            b.act_local_rotation(0, 10)

            a.cphase(0, 1)
            b.act_cz(0, 1)

            a.local_op(0, graphsim.LocCliffOp(i))
            b.act_local_rotation(0, i)
            a.local_op(1, graphsim.LocCliffOp(j))
            b.act_local_rotation(1, j)

            a.cphase(0, 1)
            b.act_cz(0, 1)

            compare(a, b)


def test_with_cphase_gates_hadamard_only(N=10):
    """ Hadamrds and CPHASEs, deterministic """

    a = graphsim.GraphRegister(N)
    b = GraphState()

    for i in range(N):
        a.hadamard(i)
        b.add_node(i)
        b.act_hadamard(i)

    for i in range(N-1):
        a.cphase(i, i+1)
        b.act_cz(i, i+1)

    compare(a, b)

def test_all(N=3):
    """ Test all gates at random """
    #TODO: Currently fails. Why???

    clifford.use_old_cz()


    a = graphsim.GraphRegister(N)
    b = GraphState(range(N))
    previous_state, previous_cz = None, None
    while isequal(a, b):
        if random.random()>0.5:
            j = random.randint(0, N-1)
            a.hadamard(j)
            b.act_hadamard(j)
        else:
            q = random.randint(0, N-2)
            a.cphase(q, q+1)
            b.act_cz(q, q+1)
            previous_state = deepcopy(b)
            previous_cz = q, q+1

    print "Initial state:"
    print previous_state.node
    print previous_state.adj
    print "CZ:", previous_cz
    print "Pete state:\n", a.get_adj_list()
    print "Anders state:\n", b.adj_list()



