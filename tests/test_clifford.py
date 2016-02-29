import clifford as lc
from numpy import *
from scipy.linalg import sqrtm
from qi import *
from tqdm import tqdm



def identify_pauli(m):
    """ Given a signed Pauli matrix, name it. """
    for sign in (+1, -1):
        for pauli_label, pauli in zip("xyz", paulis):
            if allclose(sign * pauli, m):
                return sign, pauli_label


def test_find_up_to_phase():
    """ Test that slightly suspicious function """
    assert lc.find_up_to_phase(id) == (0, 0)
    assert lc.find_up_to_phase(px) == (1, 0)
    assert lc.find_up_to_phase(exp(1j*pi/4.)*ha) == (4, 7)

def get_action(u):
    """ What does this unitary operator do to the Paulis? """
    return [identify_pauli(u * p * u.H) for p in paulis]


def format_action(action):
    return "".join("{}{}".format("+" if s >= 0 else "-", p) for s, p in action)


def test_we_have_24_matrices():
    """ Check that we have 24 unique actions on the Bloch sphere """
    actions = set(tuple(get_action(u)) for u in lc.unitaries)
    assert len(set(actions)) == 24


def test_we_have_all_useful_gates():
    """ Check that all the interesting gates are included up to a global phase """
    common_us = id, px, py, pz, ha, ph, sqz, msqz, sqy, msqy, sqx, msqx
    for u in common_us:
        lc.find_up_to_phase(u)


def test_group():
    """ Test we are really in a group """
    matches = set()
    for a in tqdm(lc.unitaries, "Testing this is a group"):
        for b in lc.unitaries:
            i, phase = lc.find_up_to_phase(a*b)
            matches.add(i)
    assert len(matches)==24


def test_conjugation_table():
    """ Check that the table of Hermitian conjugates is okay """
    assert len(set(lc.conjugation_table))==24

def test_times_table():
    """ Check the times table """
    assert lc.times_table[0][4]==4
