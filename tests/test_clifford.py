from numpy import *
from scipy.linalg import sqrtm
from tqdm import tqdm
import itertools as it
from abp import clifford
from abp import qi


def identify_pauli(m):
    """ Given a signed Pauli matrix, name it. """
    for sign in (+1, -1):
        for pauli_label, pauli in zip("xyz", qi.paulis):
            if allclose(sign * pauli, m):
                return sign, pauli_label


def _test_find():
    """ Test that slightly suspicious function """
    assert lc.find(id, lc.unitaries) == 0
    assert lc.find(px, lc.unitaries) == 1
    assert lc.find(exp(1j*pi/4.)*ha, lc.unitaries) == 4

def get_action(u):
    """ What does this unitary operator do to the Paulis? """
    return [identify_pauli(u.dot(p.dot(qi.hermitian_conjugate(u)))) for p in qi.paulis]


def format_action(action):
    return "".join("{}{}".format("+" if s >= 0 else "-", p) for s, p in action)


def test_we_have_24_matrices():
    """ Check that we have 24 unique actions on the Bloch sphere """
    actions = set(tuple(get_action(u)) for u in clifford.unitaries)
    assert len(set(actions)) == 24


def test_we_have_all_useful_gates():
    """ Check that all the interesting gates are included up to a global phase """
    for name, u in qi.by_name.items():
        clifford.find_clifford(u, clifford.unitaries)


def _test_group():
    """ Test we are really in a group """
    matches = set()
    for a, b in tqdm(it.combinations(clifford.unitaries, 2), "Testing this is a group"):
        i, phase = clifford.find_clifford(a.dot(b), clifford.unitaries)
        matches.add(i)
    assert len(matches)==24


def test_conjugation_table():
    """ Check that the table of Hermitian conjugates is okay """
    assert len(set(clifford.conjugation_table))==24

def test_times_table():
    """ Check the times table """
    assert clifford.times_table[0][4]==4
