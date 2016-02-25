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

def get_sign(x):
    """ Get the sign of a number """
    return "+" if x>=0 else "-"

def identify_pauli(m):
    """ Given a signed Pauli matrix, name it. """
    for sign_label, sign in (("+", +1), ("-", -1)):
        for pauli_label, pauli in zip("xyz", paulis):
            if allclose(sign*pauli, m):
                return "{}{}".format(sign_label, pauli_label)

def get_action(u):
    """ Get the action of a Pauli matrix on three qubits """
    return tuple(identify_pauli(u*p*u.H) for p in paulis)

def cliff_action(permutation, op):
    """ Computes the action of a particular local Clifford """


if __name__ == '__main__':
    labels =       ("a"   , "b"   , "c"   , "d"   , "e"   , "f")
    signs =        (+1    , -1    , -1    , -1    , +1    , +1)
    permutations = ("xyz" , "yxz" , "zyx" , "xzy" , "yzx" , "zxy")

    for label, sign, permutation in zip(labels, signs, permutations):
        for op in "ixyz":
            signs = [sign if (a == op or op == "i") else -sign for a in "xyz"]
            print label, op
            print tuple("{}{}".format(get_sign(x), y) for x, y in zip(signs, permutation))




            #print "{}{} = ({}, {})".format(op, label, "+" if sign>=0 else "-", permutation),
        print


    #for s, sn in zip(s_rotations, s_names):
        #for c, cn in zip(c_rotations, c_names):
            #print sn, "\t", cn, "\t", get_action(s*c)


