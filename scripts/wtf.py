from abp import clifford, qi
import numpy as np
import itertools as it

def conj_hack(operator, unitary):
    """ TODO: make this meaningful / legible """
    assert operator in set(xrange(4))
    op = clifford.times_table[unitary, operator]
    op = clifford.times_table[op, clifford.conjugation_table[unitary]]
    is_id_or_operator = (unitary % 4 == 0) or (unitary % 4 == operator)
    is_non_pauli = (unitary >= 4) and (unitary <= 15)
    phase = ((-1, 1), (1, -1))[is_id_or_operator][is_non_pauli]
    if operator == 0: 
        phase = 1
    return op, phase

def conj(operator, unitary):
    """ Better """
    matrices = ({"x": qi.msqx, "z": qi.sqz}[c] for c in clifford.decompositions[unitary])
    unitary = reduce(np.dot, matrices, np.eye(2, dtype=complex))
    operator = qi.operators[operator]
    new_operator = reduce(np.dot, (unitary, operator, qi.hermitian_conjugate(unitary)))

    for i, o in enumerate(qi.operators):
        if np.allclose(o, new_operator):
            return i, 1
        elif np.allclose(o, -new_operator):
            return i, -1

    raise IndexError


for operator, unitary in it.product(range(4), range(24)):
    assert conj(operator, unitary) == conj_hack(operator, unitary)

    #new = np.dot(u, np.dot(o, qi.hermitian_conjugate(u)))
    #which = clifford.find_clifford(new, clifford.unitaries[:4])
    #assert which in xrange(4)
    #whichm = [qi.id, qi.px, qi.py, qi.pz][which]
    #if np.allclose(new, whichm):
        #return which, 1
    #elif np.allclose(new, -whichm):
        #return which, -1
    #else:
        #raise IndexError

