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

# TODO:
# - check that we re-generate the table
# - do conjugation
# - do times table
# - write tests

from numpy import *


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
    """ Format an action as a string """
    return "".join("{}{}".format("+" if s >= 0 else "-", p) for s, p in action)


# Some two-qubit matrices
i = matrix(eye(2, dtype=complex))
px = matrix([[0, 1], [1, 0]], dtype=complex)
py = matrix([[0, -1j], [1j, 0]], dtype=complex)
pz = matrix([[1, 0], [0, -1]], dtype=complex)
h = matrix([[1, 1], [1, -1]], dtype=complex) / sqrt(2)
p = matrix([[1, 0], [0, 1j]], dtype=complex)
paulis = (px, py, pz)

# Basic single-qubit gates
s_gates = (("i", i), ("p", p), ("pp", p * p), ("ppp", p * p * p))
c_gates = [("i", i), ("h", h), ("hp", h * p), ("hpp", h * p * p),
           ("hppp", h * p * p * p), ("hpph", h * p * p * h)]

# Build the table of VOPs according to Anders (verbatim from thesis)
table = (("a", "xyz", +1), ("b", "yxz", -1), ("c", "zyx", -1),
        ("d", "xzy", -1), ("e", "yzx", +1), ("f", "zxy", +1))

# Build a big ol lookup table
vop_names = []
vop_actions = []
vop_gates = [None] * 24
vop_unitaries = [None] * 24

for label, permutation, sign in table:
    for column, operator in zip("ixyz", "i" + permutation):
        effect = [((sign if (p == column or column == "i") else -sign), p)
                  for p in permutation]
        vop_names.append(column + label)  # think we can dump "operator"
        vop_actions.append(format_action(effect))

for s_name, s_gate in s_gates:
    for c_name, c_gate in c_gates:
        u = s_gate * c_gate
        action = format_action(get_action(u))
        index = vop_actions.index(action)
        vop_gates[index] = s_name + c_name
        vop_unitaries[index] = u

# Add some more useful lookups
vop_by_name = {n: {"name":n, "index": i, "action": a, "gates": g, "unitary": u}
               for n, i, a, g, u in zip(vop_names, xrange(24), vop_actions, vop_gates, vop_unitaries)}
vop_by_action = {a: {"name": n, "index": i, "action":a, "gates": g, "unitary": u}
                 for n, i, a, g, u in zip(vop_names, xrange(24), vop_actions, vop_gates, vop_unitaries)}
