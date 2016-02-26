from numpy import *
from scipy.linalg import sqrtm

# Some two-qubit matrices
i = matrix(eye(2, dtype=complex))
px = matrix([[0, 1], [1, 0]], dtype=complex)
py = matrix([[0, -1j], [1j, 0]], dtype=complex)
pz = matrix([[1, 0], [0, -1]], dtype=complex)
h = matrix([[1, 1], [1, -1]], dtype=complex) / sqrt(2)
p = matrix([[1, 0], [0, 1j]], dtype=complex)
paulis = (px, py, pz)

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

#permuters = (i, h*p*h*pz, p*h*p*h, px*p, p*h, p*p*h*pz)
permuters = (i, h, p, h*p, h*p*h, h*p*h*p)
signs = (i, px, py, pz)
unitaries = []
actions = []
for perm in permuters:
    for sign in signs:
        action = format_action(get_action(sign*perm))
        actions.append(action)
        unitaries.append(perm*sign)
        #print (perm*sign).round(2).reshape(1,4)[0],
        print action,
    print


assert len(set(actions)) == 24

sqy = sqrtm(1j*py)
msqy = sqrtm(-1j*py)
sqz = sqrtm(1j*pz)
msqz = sqrtm(-1j*pz)
sqx = sqrtm(1j*px)
msqx = sqrtm(-1j*px)
for m in i, px, py, pz, h, p, sqz, msqz, sqy, msqy, sqx, msqx:
    if any([allclose(u, m) for u in unitaries]):
        print "found it"
    else:
        if any([allclose(exp(1j*pi*phi/4.)*u, m) for phi in range(8) for u in unitaries]):
            print "found up to global phase"
        else:
            print "lost"

