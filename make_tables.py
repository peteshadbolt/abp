#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This program generates lookup tables
"""

import qi
import numpy as np
from tqdm import tqdm
from functools import reduce
import itertools as it

DECOMPOSITIONS = ("xxxx", "xx", "zzxx", "zz", "zxx", "z", "zzz", "xxz",
     "xzx", "xzxxx", "xzzzx", "xxxzx", "xzz", "zzx", "xxx", "x",
     "zzzx", "xxzx", "zx", "zxxx", "xxxz", "xzzz", "xz", "xzxx")


def find_clifford(needle, haystack):
    """ Find the index of a given u within a list of unitaries, up to a global phase  """
    for i, t in enumerate(haystack):
        for phase in range(8):
            if np.allclose(t, np.exp(1j * phase * np.pi / 4.) * needle):
                return i
    raise IndexError


def find_cz(bond, c1, c2, z, krontable):
    """ Find the output of a CZ operation """
    # Figure out the target state
    state = qi.bond if bond else qi.nobond
    target = qi.cz.dot(krontable[c1, c2].dot(state))

    # Choose the sets to search over
    s1 = z if c1 in z else xrange(24)
    s2 = z if c2 in z else xrange(24)

    # Find a match
    for bond, c1p, c2p in it.product([0, 1], s1, s2):
        state = qi.bond if bond else qi.nobond
        trial = krontable[c1p, c2p].dot(state)
        for phase in range(8):
            if np.allclose(target, np.exp(1j * phase * np.pi / 4.) * trial):
                return bond, c1p, c2p

    # Didn't find anything - this should never happen
    raise IndexError


def compose_u(decomposition):
    """ Get the unitary representation of a particular decomposition """
    matrices = ({"x": qi.sqx, "z": qi.msqz}[c] for c in decomposition)
    return reduce(np.dot, matrices, np.matrix(np.eye(2, dtype=complex)))


def get_unitaries(decompositions):
    """ The Clifford group """
    return [compose_u(d) for d in decompositions]


def hermitian_conjugate(u):
    """ Get the hermitian conjugate """
    return np.conjugate(np.transpose(u))


def get_conjugation_table(unitaries):
    """ Construct the conjugation table """
    return np.array([find_clifford(hermitian_conjugate(u), unitaries) for u in unitaries])


def get_times_table(unitaries):
    """ Construct the times-table """
    return np.array([[find_clifford(u.dot(v), unitaries) for v in unitaries]
                   for u in tqdm(unitaries)])


def get_krontable():
    """ Cache a table of Kronecker products to speed up a little bit """
    krontable = np.zeros((24, 24, 4, 4), dtype=complex)
    for i, j in it.product(range(24), range(24)):
        krontable[i, j,:,:] = np.kron(unitaries[i], unitaries[j])
    return krontable


def get_cz_table(unitaries):
    """ Compute the lookup table for the CZ (A&B eq. 9) """
    z = (qi.id, qi.px, qi.pz, qi.ph, hermitian_conjugate(qi.ph))
    z = [find_clifford(u, unitaries) for u in z]
    krontable = get_krontable()

    cz_table = np.zeros((2, 24, 24, 3))
    for bond, c1, c2 in tqdm(list(it.product([0, 1], range(24), range(24)))):
        cz_table[bond, c1, c2] = find_cz(bond, c1, c2, z, krontable)
    return cz_table

if __name__ == '__main__':
    unitaries = get_unitaries(DECOMPOSITIONS)
    conjugation_table = get_conjugation_table(unitaries)
    times_table = get_times_table(unitaries)
    cz_table = get_cz_table(unitaries)

    np.save("tables/unitaries.npy", unitaries)
    np.save("tables/conjugation_table.npy", conjugation_table)
    np.save("tables/times_table.npy", times_table)
    np.save("cz_table.npy", cz_table)
