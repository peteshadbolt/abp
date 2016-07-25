from abp import GraphState, CircuitModel, clifford
from abp import clifford
from mock import simple_graph
import random
import numpy as np
from tqdm import tqdm

REPEATS = 100
DEPTH = 100


def test_graph_basic():
    """ Test that we can construct graphs, delete edges, whatever """
    g = simple_graph()
    assert set(g.adj[0].keys()) == set([1, 2, 3])
    g._del_edge(0, 1)
    assert set(g.adj[0].keys()) == set([2, 3])
    assert g.has_edge(1, 2)
    assert not g.has_edge(0, 1)


def test_local_complementation():
    """ Test that local complementation works as expected """
    g = simple_graph()
    g.local_complementation(0)
    assert g.has_edge(0, 1)
    assert g.has_edge(0, 2)
    assert not g.has_edge(1, 2)
    assert g.has_edge(3, 2)
    assert g.has_edge(3, 1)

    # TODO: test VOP conditions


def test_remove_vop():
    """ Test that removing VOPs really works """
    g = simple_graph()
    g.remove_vop(0, 1)
    assert g.node[0]["vop"] == clifford.by_name["identity"]
    g.remove_vop(1, 1)
    assert g.node[1]["vop"] == clifford.by_name["identity"]
    g.remove_vop(2, 1)
    assert g.node[2]["vop"] == clifford.by_name["identity"]
    g.remove_vop(0, 1)
    assert g.node[0]["vop"] == clifford.by_name["identity"]


def test_edgelist():
    """ Test making edgelists """
    g = simple_graph()
    el = g.edgelist()
    assert (0, 3) in el
    assert (0, 2) in el
    assert (100, 200) in el


def test_stress(n = int(1e5)):
    """ Testing that making a graph of ten thousand qubits takes less than half a second"""
    import time
    g = GraphState(range(n+1))
    t = time.clock()
    for i in xrange(n):
        g._add_edge(i, i + 1)
    assert time.clock() - t < .5


def test_cz():
    """ Test CZ gate """
    g = GraphState([0, 1])
    g.act_local_rotation(0, clifford.by_name["hadamard"])
    g.act_local_rotation(1, clifford.by_name["hadamard"])
    g.act_local_rotation(1, clifford.by_name["py"])
    assert not g.has_edge(0, 1)
    g.act_cz(0, 1)
    assert g.has_edge(0, 1)

def test_stabilizer():
    """ Test that we can generate stabilizers okay """
    g = simple_graph()
    stab = g.to_stabilizer()
    #TODO

def test_local_complementation():
    """ Test that local complementation works okay """
    psi = GraphState()
    psi.add_node(0)
    psi.add_node(1)
    psi.add_node(2)
    psi.add_node(3)

    for n in psi.node:
        psi.act_hadamard(n)

    psi.act_cz(0, 1)
    psi.act_cz(0, 3)
    psi.act_cz(1, 3)
    psi.act_cz(1, 2)

    old_edges = psi.edgelist()
    old_state = psi.to_state_vector()
    psi.local_complementation(1)
    assert old_edges != psi.edgelist()
    assert old_state == psi.to_state_vector()

def test_single_qubit():
    """ A multi qubit test with Hadamards only"""
    for repeat in tqdm(range(REPEATS), desc="Testing against circuit model"):
        g = GraphState([0])
        c = CircuitModel(1)

        for i in range(100):
            op = np.random.choice(range(24))
            g.act_local_rotation(0, op)
            c.act_local_rotation(0, clifford.unitaries[op])

        assert g.to_state_vector() == c


def test_hadamard_only_multiqubit(n=6):
    """ A multi qubit test with Hadamards only"""
    for repeat in tqdm(range(REPEATS), desc="Testing against circuit model"):
        g = GraphState(range(n))
        c = CircuitModel(n)

        for i in range(n):
            g.act_hadamard(i)
            c.act_hadamard(i)

        assert g.to_state_vector() == c

        for i in range(100):
            a, b = np.random.choice(range(n), 2, False)
            g.act_cz(a, b)
            c.act_cz(a, b)

        assert g.to_state_vector() == c


def test_all_multiqubit(n=4):
    """ A multi qubit test with arbitrary local rotations """
    g = GraphState(range(n))
    c = CircuitModel(n)
    for i in range(10):
        qubit = np.random.randint(0, n - 1)
        rotation = np.random.randint(0, 24 - 1)
        g.act_local_rotation(qubit, rotation)
        c.act_local_rotation(qubit, clifford.unitaries[rotation])

    assert g.to_state_vector() == c

    for repeat in tqdm(range(REPEATS), desc="Testing against circuit model"):
        a, b = np.random.choice(range(n), 2, False)
        g.act_cz(a, b)
        c.act_cz(a, b)
        assert np.allclose(np.sum(np.abs(c.state) ** 2), 1)
        assert np.allclose(
            np.sum(np.abs(g.to_state_vector().state) ** 2), 1)

        assert g.to_state_vector() == c

    assert g.to_state_vector() == c

def test_all(n=8):
    """ A multi qubit test with arbitrary local rotations """
    g = GraphState(range(n))
    c = CircuitModel(n)
    for repeat in tqdm(xrange(REPEATS), "Testing against circuit model"):
        for step in xrange(DEPTH):
            if random.random()>0.5:
                qubit = np.random.randint(0, n - 1)
                rotation = np.random.randint(0, 24 - 1)
                g.act_local_rotation(qubit, rotation)
                c.act_local_rotation(qubit, clifford.unitaries[rotation])
            else:
                a, b = np.random.choice(range(n), 2, False)
                g.act_cz(a, b)
                c.act_cz(a, b)
        assert g.to_state_vector() == c


