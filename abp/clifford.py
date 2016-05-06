#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This program generates lookup tables
"""

import os, json
from functools import reduce
import itertools as it
from . import qi
import numpy as np
import tempfile
from tqdm import tqdm

decompositions = ("xxxx", "xx", "zzxx", "zz", "zxx", "z", "zzz", "xxz",
                  "xzx", "xzxxx", "xzzzx", "xxxzx", "xzz", "zzx", "xxx", "x",
                  "zzzx", "xxzx", "zx", "zxxx", "xxxz", "xzzz", "xz", "xzxx")


def find_clifford(needle, haystack):
    """ Find the index of a given u within a list of unitaries, up to a global phase  """
    needle = normalize_global_phase(needle)
    for i, t in enumerate(haystack):
        if np.allclose(t, needle):
            return i
    raise IndexError


def normalize_global_phase(m):
    """ Normalize the global phase of a matrix """
    v = (x for x in m.flatten() if np.abs(x) > 0.001).next()
    phase = np.arctan2(v.imag, v.real) % np.pi
    rot = np.exp(-1j * phase)
    return rot * m if rot * v > 0 else -rot * m


def find_cz(bond, c1, c2, commuters, state_table):
    """ Find the output of a CZ operation """
    # Figure out the target state
    target = qi.cz.dot(state_table[bond, c1, c2])
    target = normalize_global_phase(target)

    # Choose the sets to search over
    s1 = commuters if c1 in commuters else xrange(24)
    s2 = commuters if c2 in commuters else xrange(24)

    # Find a match
    for bond, c1p, c2p in it.product([0, 1], s1, s2):
        if np.allclose(target, state_table[bond, c1p, c2p]):
            return bond, c1p, c2p

    # Didn't find anything - this should never happen
    raise IndexError


def compose_u(decomposition):
    """ Get the unitary representation of a particular decomposition """
    matrices = ({"x": qi.sqx, "z": qi.msqz}[c] for c in decomposition)
    output = reduce(np.dot, matrices, np.eye(2, dtype=complex))
    return normalize_global_phase(output)


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
        state_table[bond, i, j, :] = normalize_global_phase(
            np.dot(kp, state).T)
    return state_table


def get_cz_table(unitaries):
    """ Compute the lookup table for the CZ (A&B eq. 9) """
    # This is the set of Cliffords which commute with CZ
    commuters = (qi.id, qi.px, qi.pz, qi.ph, qi.hermitian_conjugate(qi.ph))
    commuters = [find_clifford(u, unitaries) for u in commuters]

    # Get a cached state table
    state_table = get_state_table(unitaries)

    # And now build the CZ table
    cz_table = np.zeros((2, 24, 24, 3))
    rows = list(it.product([0, 1], it.combinations(range(24), 2)))
                # CZ is symmetric so we only need combinations
    for bond, (c1, c2) in tqdm(rows, desc="Building CZ table"):
        newbond, c1p, c2p = find_cz(bond, c1, c2, commuters, state_table)
        cz_table[bond, c1, c2] = [newbond, c1p, c2p]
        cz_table[bond, c2, c1] = [newbond, c2p, c1p]
    return cz_table


# First try to load tables from cache. If that fails, build them from
# scratch and store
os.chdir(tempfile.gettempdir())
try:
    unitaries = np.load("unitaries.npy")
    conjugation_table = np.load("conjugation_table.npy")
    times_table = np.load("times_table.npy")
    cz_table = np.load("cz_table.npy")

    with open("by_name.json") as f:
        by_name = json.load(f)

    print "Loaded tables from cache"
except IOError:
    # Spend time building the tables
    unitaries = get_unitaries()
    by_name = get_by_name(unitaries)
    conjugation_table = get_conjugation_table(unitaries)
    times_table = get_times_table(unitaries)
    cz_table = get_cz_table(unitaries)

    # Write it all to disk
    np.save("unitaries.npy", unitaries)
    np.save("conjugation_table.npy", conjugation_table)
    np.save("times_table.npy", times_table)
    np.save("cz_table.npy", cz_table)

    with open("by_name.json", "wb") as f:
        json.dump(by_name, f)
