from abp import GraphState, CircuitModel, clifford
from anders_briegel import graphsim
import numpy as np
from numpy import random
from tqdm import tqdm
import itertools as it
import mock

REPEATS = 100
DEPTH = 100

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
        circuit = [(mock.random_pair(n), gate) if gate =="cz" 
                   else (random.choice(range(n)), gate)
                   for gate in circuit]
        mock.test_circuit(circuit, n)

def test_all(n=10):
    """ Test everything"""
    for i in tqdm(range(REPEATS), desc="Testing CZ and Hadamard against A&B"):
        circuit = random.choice(["cz"]*10 + range(24), DEPTH)
        circuit = [(mock.random_pair(n), gate) if gate =="cz" 
                   else (random.choice(range(n)), gate)
                   for gate in circuit]
        mock.test_circuit(circuit, n)


