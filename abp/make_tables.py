#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This program generates lookup tables
"""

import os, json
from functools import reduce
import itertools as it
import qi
import numpy as np
from tqdm import tqdm
from clifford import decompositions


def find_clifford(needle, haystack):
    """ Find the index of a given u within a list of unitaries, up to a global phase  """
    for i, t in enumerate(haystack):
        for phase in range(8):
            if np.allclose(t, np.exp(1j * phase * np.pi / 4.) * needle):
                return i
    raise IndexError


def find_cz(bond, c1, c2, commuters, state_table):
    """ Find the output of a CZ operation """
    # Figure out the target state
    state = qi.bond if bond else qi.nobond
    target = qi.cz.dot(state_table[bond, c1, c2])

    # Choose the sets to search over
    s1 = commuters if c1 in commuters else xrange(24)
    s2 = commuters if c2 in commuters else xrange(24)

    # Find a match
    for bond, c1p, c2p in it.product([0, 1], s1, s2):
        trial = state_table[bond, c1p, c2p]
        for phase in range(8):
            if np.allclose(target, np.exp(1j * phase * np.pi / 4.) * trial):
                return bond, c1p, c2p

    # Didn't find anything - this should never happen
    raise IndexError


def compose_u(decomposition):
    """ Get the unitary representation of a particular decomposition """
    matrices = ({"x": qi.sqx, "z": qi.msqz}[c] for c in decomposition)
    return reduce(np.dot, matrices, np.matrix(np.eye(2, dtype=complex)))


def get_unitaries():
    """ The Clifford group """
    return [compose_u(d) for d in decompositions]


def get_by_name(unitaries):
    """ Get a lookup table of cliffords by name """
    return {name: find_clifford(u, unitaries)
            for name, u in qi.by_name.items()}


def get_conjugation_table(unitaries):
    """ Construct the conjugation table """
    return np.array([find_clifford(qi.hermitian_conjugate(u), unitaries) for u in unitaries])


def get_times_table(unitaries):
    """ Construct the times-table """
    return np.array([[find_clifford(u.dot(v), unitaries) for v in unitaries]
                     for u in tqdm(unitaries, desc="Building times-table")])


def get_state_table(unitaries):
    """ Cache a table of state to speed up a little bit """
    state_table = np.zeros((2, 24, 24, 4), dtype=complex)
    params = list(it.product([0, 1], range(24), range(24)))
    for bond, i, j in tqdm(params, desc="Building state table"):
        state = qi.bond if bond else qi.nobond
        kp = np.kron(unitaries[i], unitaries[j])
        state_table[bond, i, j, :] = np.dot(kp, state).T
    return state_table


def get_cz_table(unitaries):
    """ Compute the lookup table for the CZ (A&B eq. 9) """
    commuters = (qi.id, qi.px, qi.pz, qi.ph, qi.hermitian_conjugate(qi.ph))
    commuters = [find_clifford(u, unitaries) for u in commuters]
    state_table = get_state_table(unitaries)

    # TODO: it's symmetric. this can be much faster
    cz_table = np.zeros((2, 24, 24, 3))
    rows = list(it.product([0, 1], range(24), range(24)))
    for bond, c1, c2 in tqdm(rows, desc="Building CZ table"):
        cz_table[bond, c1, c2] = find_cz(bond, c1, c2, commuters, state_table)
    return cz_table


if __name__ == "__main__":
    # Spend time loading the stuff
    unitaries = get_unitaries()
    by_name = get_by_name(unitaries)
    conjugation_table = get_conjugation_table(unitaries)
    times_table = get_times_table(unitaries)
    #cz_table = get_cz_table(unitaries)

    # Write it all to disk
    directory = os.path.dirname(os.path.abspath(__file__))
    where = os.path.join(directory, "tables/")
    os.chdir(where)
    np.save("unitaries.npy", unitaries)
    np.save("conjugation_table.npy", conjugation_table)
    np.save("times_table.npy", times_table)
    #np.save("cz_table.npy", cz_table)

    with open("by_name.json", "wb") as f:
        json.dump(by_name, f)

