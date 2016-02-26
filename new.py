from numpy import *

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

#print get_action(i)
#print get_action(px)
#print get_action(py)
#print get_action(pz)

permuters = 

print format_action(get_action(i))
print format_action(get_action(h*p*h*pz))
print format_action(get_action(p*h*p*h))
print format_action(get_action(px*p))
print format_action(get_action(p*h))
print format_action(get_action(p*p*h*pz))

