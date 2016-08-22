from abp import GraphState, CircuitModel, clifford
import mock
import random
import numpy as np
from tqdm import tqdm
import networkx as nx

REPEATS = 100
DEPTH = 100

def test_initialization():
    g = GraphState("abc")
    assert g.node["a"]["vop"] == clifford.by_name["identity"]
    g = GraphState("abc", vop="hadamard")
    assert g.node["c"]["vop"] == clifford.by_name["hadamard"]
    g = GraphState(5)
    assert len(g.node) == 5


def test_graph_basic():
    """ Test that we can construct graphs, delete edges, whatever """
    g = mock.simple_graph()
    assert set(g.adj[0].keys()) == set([1, 2, 3])
    g._del_edge(0, 1)
    assert set(g.adj[0].keys()) == set([2, 3])
    assert g.has_edge(1, 2)
    assert not g.has_edge(0, 1)


def test_local_complementation():
    """ Test that local complementation works as expected """
    g = mock.simple_graph()
    g.local_complementation(0)
    assert g.has_edge(0, 1)
    assert g.has_edge(0, 2)
    assert not g.has_edge(1, 2)
    assert g.has_edge(3, 2)
    assert g.has_edge(3, 1)

    # TODO: test VOP conditions


def test_remove_vop():
    """ Test that removing VOPs really works """
    g = mock.simple_graph()
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
    g = mock.simple_graph()
    el = g.edgelist()
    assert (0, 3) in el
    assert (0, 2) in el
    assert (100, 200) in el


def test_stress(n=int(1e5)):
    """ Testing that making a graph of ten thousand qubits takes less than half a second"""
    import time
    g = GraphState(range(n + 1), vop="hadamard")
    t = time.clock()
    for i in xrange(n):
        g._add_edge(i, i + 1)
    assert time.clock() - t < .5


def test_cz():
    """ Test CZ gate """
    g = GraphState([0, 1], vop="hadamard")
    g.act_local_rotation(0, clifford.by_name["hadamard"])
    g.act_local_rotation(1, clifford.by_name["hadamard"])
    g.act_local_rotation(1, clifford.by_name["py"])
    assert not g.has_edge(0, 1)
    g.act_cz(0, 1)
    assert g.has_edge(0, 1)


def test_local_complementation():
    """ Test that local complementation works okay """
    pairs = (0, 1), (0, 3), (1, 3), (1, 2), 
    psi = GraphState(range(4), vop="hadamard")
    psi.act_circuit([(i, "hadamard") for i in psi.node])
    psi.act_circuit([(pair, "cz") for pair in pairs])
    old_edges = psi.edgelist()
    old_state = psi.to_state_vector()
    psi.local_complementation(1)
    assert old_edges != psi.edgelist()
    assert old_state == psi.to_state_vector()


def test_single_qubit():
    """ A multi qubit test with Hadamards only"""
    for repeat in tqdm(range(REPEATS), desc="Single qubit rotations against CircuitModel"):
        circuit = [(0, random.choice(range(24))) for i in range(DEPTH)]
        a = mock.circuit_to_state(mock.ABPWrapper, 1, circuit)
        b = mock.circuit_to_state(mock.CircuitModelWrapper, 1, circuit)
        assert a.to_state_vector() == b


def test_graph_state_multiqubit(n=6):
    """ A multi qubit test with Hadamards only"""
    for repeat in tqdm(range(REPEATS), desc="Random graph states against the CircuitModel"):
        circuit = mock.random_graph_circuit(n)
        a = mock.circuit_to_state(mock.ABPWrapper, n, circuit)
        b = mock.circuit_to_state(mock.CircuitModelWrapper, n, circuit)
        assert a.to_state_vector() == b


def test_stabilizer_state_multiqubit(n=6):
    """ A multi qubit test with arbitrary local rotations """
    for repeat in tqdm(range(REPEATS), desc="Random Clifford circuits against the CircuitModel"):
        circuit = mock.random_stabilizer_circuit(n)
        a = mock.circuit_to_state(mock.ABPWrapper, n, circuit)
        b = mock.circuit_to_state(mock.CircuitModelWrapper, n, circuit)
        assert a.to_state_vector() == b


def test_from_nx():
    """ Creating from a networkx graph """
    g = nx.random_geometric_graph(100, 2)
    psi = GraphState(g)
    assert len(psi.node) == 100

    psi = GraphState(nx.Graph(((0, 1),)))

