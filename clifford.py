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

def find_up_to_phase(u):
    """ Find the index of a given u within a list of unitaries, up to a global phase  """
    global unitaries
    for i, t in enumerate(unitaries):
        for phase in range(8):
            if allclose(t, exp(1j*phase*pi/4.)*u):
                return i, phase
    raise IndexError

id = matrix(eye(2, dtype=complex))
px = matrix([[0, 1], [1, 0]], dtype=complex)
py = matrix([[0, -1j], [1j, 0]], dtype=complex)
pz = matrix([[1, 0], [0, -1]], dtype=complex)
ha = matrix([[1, 1], [1, -1]], dtype=complex) / sqrt(2)
ph= matrix([[1, 0], [0, 1j]], dtype=complex)

permutations = (id, ha, ph, ha*ph, ha*ph*ha, ha*ph*ha*ph)
signs = (id, px, py, pz)
unitaries = [p*s for p in permutations for s in signs]

conjugation_table = []

for i, u in enumerate(unitaries):
    i, phase = find_up_to_phase(u.H)
    conjugation_table.append(i)


# TODO:
# - check that we re-generate the table
# - do conjugation
# - do times table
# - write tests

