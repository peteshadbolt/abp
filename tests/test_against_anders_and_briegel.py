from abp import GraphState
from anders_briegel import graphsim
from abp import CircuitModel
from abp import clifford
import random
import numpy as np
from tqdm import tqdm

REPEATS = 100000

def assert_equal(a, b, debug=""):
    assert a.to_json() == b.to_json()

def test_hadamard():
    """ Test hadamards """
    a = graphsim.GraphRegister(1)
    b = GraphState()
    b.add_node(0)

    assert_equal(a, b)
    a.hadamard(0)
    b.act_hadamard(0)
    assert_equal(a, b)
    a.hadamard(0)
    b.act_hadamard(0)
    assert_equal(a, b)


def test_local_rotations():
    """ Test local rotations """
    a = graphsim.GraphRegister(1)
    b = GraphState()
    b.add_node(0)
    assert_equal(a, b)

    for i in range(1000):
        j = random.randint(0, 23)
        a.local_op(0, graphsim.LocCliffOp(j))
        b.act_local_rotation(0, j)
        assert_equal(a, b)


def test_times_table():
    """ Test times table """
    for i, j in it.product(range(24), range(24)):
        a = graphsim.GraphRegister(1)
        b = GraphState([0])
        a.local_op(0, graphsim.LocCliffOp(i))
        a.local_op(0, graphsim.LocCliffOp(j))
        b.act_local_rotation(0, i)
        b.act_local_rotation(0, j)
        assert_equal(a, b)


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

            assert_equal(a, b)

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

            assert_equal(a, b)


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

    assert_equal(a, b)

def test_cz_hadamard(N=10):
    """ Test CZs and Hadamards at random """

    clifford.use_old_cz()

    a = graphsim.GraphRegister(N)
    b = GraphState(range(N))
    for i in tqdm(range(REPEATS), desc="Testing CZ and Hadamard against A&B"):
        if random.random()>0.5:
            j = random.randint(0, N-1)
            a.hadamard(j)
            b.act_hadamard(j)
        else:
            q = random.randint(0, N-2)
            a.cphase(q, q+1)
            b.act_cz(q, q+1)
        assert_equal(a, b)



def test_all(N=9):
    """ Test everything"""

    clifford.use_old_cz()

    a = graphsim.GraphRegister(N)
    b = GraphState(range(N))
    print "woi"
    for i in tqdm(range(REPEATS), desc="Testing all gates against Anders and Briegel"):
        if random.random()>0.5:
            j = random.randint(0, N-1)
            u = random.randint(0, 23)
            a.local_op(j, graphsim.LocCliffOp(u))
            b.act_local_rotation(j, u)
        else:
            q = random.randint(0, N-2)
            a.cphase(q, q+1)
            b.act_cz(q, q+1)
        assert_equal(a, b, str(i))


