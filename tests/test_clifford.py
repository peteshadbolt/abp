import clifford as lc
from numpy import *
from scipy.linalg import sqrtm

sqy = sqrtm(1j * lc.py)
msqy = sqrtm(-1j * lc.py)
sqz = sqrtm(1j * lc.pz)
msqz = sqrtm(-1j * lc.pz)
sqx = sqrtm(1j * lc.px)
msqx = sqrtm(-1j * lc.px)
paulis = (lc.px, lc.py, lc.pz)


def identify_pauli(m):
    """ Given a signed Pauli matrix, name it. """
    for sign in (+1, -1):
        for pauli_label, pauli in zip("xyz", paulis):
            if allclose(sign * pauli, m):
                return sign, pauli_label


def test_find_up_to_phase():
    """ Test that slightly suspicious function """
    assert lc.find_up_to_phase(lc.id) == (0, 0)
    assert lc.find_up_to_phase(lc.px) == (1, 0)
    assert lc.find_up_to_phase(exp(1j*pi/4.)*lc.ha) == (4, 7)

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
    common_us = lc.id, lc.px, lc.py, lc.pz, lc.ha, lc.ph, sqz, msqz, sqy, msqy, sqx, msqx
    for u in common_us:
        lc.find_up_to_phase(u)


def test_group():
    """ Test we are really in a group """
    matches = set()
    for a in lc.unitaries:
        for b in lc.unitaries:
            i, phase = lc.find_up_to_phase(a*b)
            matches.add(i)
    assert len(matches)==24


def test_conjugation_table():
    """ Check that the table of Hermitian conjugates is okay """
    assert len(set(lc.conjugation_table))==24

