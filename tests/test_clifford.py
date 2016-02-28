import clifford as lc
from numpy import *
from scipy.linalg import sqrtm

sqy = sqrtm(1j*lc.py)
msqy = sqrtm(-1j*lc.py)
sqz = sqrtm(1j*lc.pz)
msqz = sqrtm(-1j*lc.pz)
sqx = sqrtm(1j*lc.px)
msqx = sqrtm(-1j*lc.px)
paulis = (lc.px, lc.py, lc.pz)

def identify_pauli(m):
    """ Given a signed Pauli matrix, name it. """
    for sign in (+1, -1):
        for pauli_label, pauli in zip("xyz", paulis):
            if allclose(sign * pauli, m):
                return sign, pauli_label

def get_action(u):
    """ What does this unitary operator do to the Paulis? """
    return [identify_pauli(u * p * u.H) for p in paulis]

def format_action(action):
    return "".join("{}{}".format("+" if s>=0 else "-", p) for s, p in action)


def test_we_have_all_useful_gates():
    """ Check that all the interesting gates are included up to a global phase """
    names = "i", "px", "py", "pz", "h", "p"
    unitaries = lc.i, lc.px, lc.py, lc.pz, lc.h, lc.p
    for name, unitary in zip(names, unitaries):
        foundit = False
        for i, clifford in enumerate(lc.unitaries):
            if allclose(clifford, unitary): 
                foundit = True
                print "{}\t=\tlc.unitaries[{}]".format(name, i)
        assert foundit

    names = "sqrt(ix)", "sqrt(-ix)", "sqrt(iy)", "sqrt(-iy)", "sqrt(iz)", "sqrt(-iz)", 
    unitaries = sqz, msqz, sqy, msqy, sqx, msqx
    for name, unitary in zip(names, unitaries):
        foundit = False
        for phase in range(8):
            for i, clifford in enumerate(lc.unitaries):
                if allclose(exp(1j*phase*pi/4.)*clifford, unitary): 
                    foundit = True
                    print "{}\t=\texp({} . i . pi/4).lc.unitaries[{}]".format(name, phase, i)
        assert foundit


def test_we_have_24_matrices():
    """ Check that we have 24 unique actions on the Bloch sphere """
    actions = set(tuple(get_action(u)) for u in lc.unitaries)
    assert len(set(actions)) == 24

