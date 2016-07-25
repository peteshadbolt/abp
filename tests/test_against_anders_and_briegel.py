from abp import GraphState, CircuitModel, clifford
from anders_briegel import graphsim
import numpy as np
from numpy import random
from tqdm import tqdm
import itertools as it
import mock

REPEATS = 100
DEPTH = 100
PAULIS = ("px", "py", "pz")

def test_hadamard():
    """ Test hadamards """
    circuit = [(0, "hadamard")]
    mock.test_circuit(circuit, 1)


def test_local_rotations():
    """ Test local rotations """
    for i in tqdm(range(REPEATS), "Testing local rotations"):
        circuit = [(0, random.choice(range(24))) for j in range(DEPTH)]
        mock.test_circuit(circuit, 1)


def test_times_table():
    """ Test times table """
    for i, j in it.product(range(24), range(24)):
        circuit = [(0, i), (0, j)]
        mock.test_circuit(circuit, 1)


def test_cz_table():
    """ Test the CZ table """
    for i, j in it.product(range(24), range(24)):
        circuit = [(0, i), (1, j), ((0, 1), "cz")]
        mock.test_circuit(circuit, 2)


def test_cz_hadamard(n=10):
    """ Test CZs and Hadamards at random """
    for i in tqdm(range(REPEATS), desc="Testing CZ and Hadamard against A&B"):
        circuit = random.choice(["cz", "hadamard"], DEPTH)
        circuit = [(mock.random_pair(n), gate) if gate == "cz"
                   else (random.choice(range(n)), gate)
                   for gate in circuit]
        mock.test_circuit(circuit, n)


def test_all(n=10):
    """ Test everything """
    for i in tqdm(range(REPEATS), desc="Testing CZ and Hadamard against A&B"):
        circuit = random.choice(["cz"] * 10 + range(24), DEPTH)
        circuit = [(mock.random_pair(n), gate) if gate == "cz"
                   else (random.choice(range(n)), gate)
                   for gate in circuit]
        mock.test_circuit(circuit, n)


def test_single_qubit_measurement():
    """ Determinstic test of all single-qubit situations """
    space = it.product(range(24), PAULIS, (0, 1))
    for rotation, measurement, outcome in tqdm(space, "Testing single qubit measurements"):
        a = mock.circuit_to_state(mock.ABPWrapper, 1, [(0, rotation)])
        b = mock.circuit_to_state(mock.AndersWrapper, 1, [(0, rotation)])
        result_a = a.measure(0, measurement, outcome)
        result_b = b.measure(0, measurement, outcome)
        assert result_a == result_b
        assert a == b

def test_two_qubit_measurement():
    """ Various two-qubit measurements on a Bell state"""
    for measurement, outcome in it.product(PAULIS, (0, 1)):
        circuit = mock.bell_pair()
        a = mock.circuit_to_state(mock.ABPWrapper, 2, circuit)
        b = mock.circuit_to_state(mock.AndersWrapper, 2, circuit)
        assert a.measure(0, measurement, outcome) == \
               b.measure(0, measurement, outcome)
        assert a == b
                
def test_graph_state_measurement(n = 10):
    """ Measuring random graph states """
    space = list(it.product(range(REPEATS), PAULIS, (0, 1)))
    for i, measurement, outcome in tqdm(space, "Measuring random graph states"):
        circuit = mock.random_graph_circuit(n, DEPTH)
        a = mock.circuit_to_state(mock.ABPWrapper, n, circuit)
        b = mock.circuit_to_state(mock.AndersWrapper, n, circuit)
        a.measure(0, measurement, outcome)
        b.measure(0, measurement, outcome)
        assert a == b

def test_stabilizer_state_measurement(n = 10):
    """ Measuring random stabilizer states """
    space = list(it.product(range(REPEATS), PAULIS, (0, 1)))
    for i, measurement, outcome in tqdm(space, "Measuring random stabilizer states"):
        circuit = mock.random_stabilizer_circuit(n, DEPTH)
        a = mock.circuit_to_state(mock.ABPWrapper, n, circuit)
        b = mock.circuit_to_state(mock.AndersWrapper, n, circuit)
        a.measure(0, measurement, outcome)
        b.measure(0, measurement, outcome)
        assert a == b
                    

