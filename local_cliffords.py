 #!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Generates and enumerates the 24 elements of the local Clifford group
Following the prescription of Anders (thesis pg. 26):
> Table 2.1: The 24 elements of the local Clifford group. The row index (here called the “sign symbol”) shows how the operator
> U permutes the Pauli operators σ = X, Y, Z under the conjugation σ = ±UσU† . The column index (the “permutation
> symbol”) indicates the sign obtained under the conjugation: For operators U in the I column it is the sign of the permutation
> (indicated on the left). For elements in the X, Y and Z columns, it is this sign only if the conjugated Pauli operator is the one
> indicated by the column header and the opposite sign otherwise.
""" 

from numpy import *

# Some two-qubit matrices
i = matrix(eye(2, dtype=complex))
px = matrix([[0, 1], [1, 0]], dtype=complex)
py = matrix([[0, -1j], [1j, 0]], dtype=complex)
pz = matrix([[1, 0], [0, -1]], dtype=complex)
h = matrix([[1, 1], [1, -1]], dtype=complex) / sqrt(2)
p = matrix([[1, 0], [0, 1j]], dtype=complex)
paulis = (px, py, pz)

# More two-qubit matrices
s_rotations = [i, p, p*p, p*p*p]
s_names = ["i", "p", "pp", "ppp"]
c_rotations = [i, h, h*p, h*p*p, h*p*p*p, h*p*p*h]
c_names = ["i", "h", "hp", "hpp", "hppp", "hpph"]

def identify_pauli(m):
    """ Given a signed Pauli matrix, name it. """
    for sign in [+1, -1]:
        for label, pauli in zip("xyz", paulis):
            if allclose(sign*pauli, m):
                return "{}{}".format("+" if sign>0 else "-", label)

def get_action(u):
    """ Get the action of a Pauli matrix on three qubits """
    return tuple(identify_pauli(u*p*u.H) for p in paulis)




if __name__ == '__main__':
    permutations = ["xyz", "yxz", "zyx", "xzy", "yzx", "zxy"]


    #for s, sn in zip(s_rotations, s_names):
        #for c, cn in zip(c_rotations, c_names):
            #print sn, "\t", cn, "\t", get_action(s*c)


