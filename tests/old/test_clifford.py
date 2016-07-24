from numpy import *
from tqdm import tqdm
import itertools as it
from abp import clifford
from abp import build_tables
from abp import qi
from nose.tools import raises


def identify_pauli(m):
    """ Given a signed Pauli matrix, name it. """
    for sign in (+1, -1):
        for pauli_label, pauli in zip("xyz", qi.paulis):
            if allclose(sign * pauli, m):
                return sign, pauli_label


def test_find_clifford():
    """ Test that slightly suspicious function """
    assert build_tables.find_clifford(qi.id, clifford.unitaries) == 0
    assert build_tables.find_clifford(qi.px, clifford.unitaries) == 1


@raises(IndexError)
def test_find_non_clifford():
    """ Test that looking for a non-Clifford gate fails """
    build_tables.find_clifford(qi.t, clifford.unitaries)


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
        build_tables.find_clifford(u, clifford.unitaries)


def test_group():
    """ Test we are really in a group """
    matches = set()
    for a, b in tqdm(it.combinations(clifford.unitaries, 2), "Testing this is a group"):
        i = build_tables.find_clifford(a.dot(b), clifford.unitaries)
        matches.add(i)
    assert len(matches) == 24


def test_conjugation_table():
    """ Check that the table of Hermitian conjugates is okay """
    assert len(set(clifford.conjugation_table)) == 24


def test_cz_table_makes_sense():
    """ Test the CZ table is symmetric """
    hadamard = clifford.by_name["hadamard"]
    assert all(clifford.cz_table[0, 0, 0] == [1, 0, 0])
    assert all(clifford.cz_table[1, 0, 0] == [0, 0, 0])
    assert all(
        clifford.cz_table[0, hadamard, hadamard] == [0, hadamard, hadamard])

def test_commuters():
    """ Test that commutation is good """
    assert len(build_tables.get_commuters(clifford.unitaries)) == 4
