# -*- coding: utf-8 -*-

"""
This program generates lookup tables and handles the Clifford group
"""

import os, json, tempfile, os, sys, json, string
from functools import reduce
import itertools as it
import numpy as np
from tqdm import tqdm
#import argparse

import qi

decompositions = ("xxxx", "xx", "zzxx", "zz", "zxx", "z", "zzz", "xxz",
                  "xzx", "xzxxx", "xzzzx", "xxxzx", "xzz", "zzx", "xxx", "x",
                  "zzzx", "xxzx", "zx", "zxxx", "xxxz", "xzzz", "xz", "xzxx")


def get_name(i):
    """ Get the human-readable name of this clifford """
    return "IXYZ"[i & 0x03] + "ABCDEF"[i / 4]


def find_clifford(needle, haystack):
    """ Find the index of a given u within a list of unitaries, up to a global phase  """
    needle = qi.normalize_global_phase(needle)
    for i, t in enumerate(haystack):
        if np.allclose(t, needle):
            return i
    raise IndexError


def find_cz(bond, c1, c2, commuters, state_table):
    """ Find the output of a CZ operation """
    # Figure out the target state
    target = qi.cz.dot(state_table[bond, c1, c2])
    target = qi.normalize_global_phase(target)

    # Choose the sets to search over
    s1 = commuters if c1 in commuters else xrange(24)
    s2 = commuters if c2 in commuters else xrange(24)

    # Find a match
    for bondp, c1p, c2p in it.product([0, 1], s1, s2):
        if np.allclose(target, state_table[bondp, c1p, c2p]):
            return bondp, c1p, c2p

    # Didn't find anything - this should never happen
    raise IndexError


def compose_u(decomposition):
    """ Get the unitary representation of a particular decomposition """
    matrices = ({"x": qi.msqx, "z": qi.sqz}[c] for c in decomposition)
    output = reduce(np.dot, matrices, np.eye(2, dtype=complex))
    return qi.normalize_global_phase(output)


def get_unitaries():
    """ The Clifford group """
    return [compose_u(d) for d in decompositions]


def get_by_name(unitaries):
    """ Get a lookup table of cliffords by name """
    a = {name: find_clifford(u, unitaries)
         for name, u in qi.by_name.items()}
    b = {get_name(i): i for i in range(24)}
    a.update(b)
    return a


def get_conjugation_table(unitaries):
    """ Construct the conjugation table """
    return np.array([find_clifford(qi.hermitian_conjugate(u), unitaries) for u in unitaries], dtype=int)


def get_times_table(unitaries):
    """ Construct the times-table """
    return np.array([[find_clifford(u.dot(v), unitaries) for v in unitaries]
                     for u in tqdm(unitaries, desc="Building times-table")], dtype=int)


def get_state_table(unitaries):
    """ Cache a table of state to speed up a little bit """
    state_table = np.zeros((2, 24, 24, 4), dtype=complex)
    params = list(it.product([0, 1], range(24), range(24)))
    for bond, i, j in tqdm(params, desc="Building state table"):
        state = qi.bond if bond else qi.nobond
        kp = np.kron(unitaries[i], unitaries[j])
        state_table[bond, i, j, :] = qi.normalize_global_phase(
            np.dot(kp, state).T)
    return state_table


def get_commuters(unitaries):
    """ Get the indeces of gates which commute with CZ """
    commuters = (qi.id, qi.pz, qi.ph, qi.hermitian_conjugate(qi.ph))
    return [find_clifford(u, unitaries) for u in commuters]


def get_cz_table(unitaries):
    """ Compute the lookup table for the CZ (A&B eq. 9) """
    # Get a cached state table and a list of gates which commute with CZ
    commuters = get_commuters(unitaries)
    state_table = get_state_table(unitaries)

    # And now build the CZ table
    cz_table = np.zeros((2, 24, 24, 3), dtype=int)
    rows = list(
        it.product([0, 1], it.combinations_with_replacement(range(24), 2)))
                # CZ is symmetric so we only need combinations
    for bond, (c1, c2) in tqdm(rows, desc="Building CZ table"):
        newbond, c1p, c2p = find_cz(
            bond, c1, c2, commuters, state_table)
        cz_table[bond, c1, c2] = [newbond, c1p, c2p]
        cz_table[bond, c2, c1] = [newbond, c2p, c1p]
    return cz_table


# First try to load tables from cache. If that fails, build them from
# scratch and store in /tmp/
tempdir = tempfile.gettempdir()
temp = lambda filename: os.path.join(tempdir, filename)
try:
    if __name__ == "__main__":
        raise IOError

    # Parse command line args
    #parser = argparse.ArgumentParser()
    #parser.add_argument("-l", "--legacy", help="Use legacy CZ table", action="store_true", default=False)
    #args = parser.parse_args()
    legacy_cz = False

    unitaries = np.load(temp("unitaries.npy"))
    conjugation_table = np.load(temp("conjugation_table.npy"))
    times_table = np.load(temp("times_table.npy"))
    if legacy_cz:
        import anders_cz
        cz_table = anders_cz.cz_table
    else:
        cz_table = np.load(temp("cz_table.npy"))

    with open(temp("by_name.json")) as f:
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
    np.save(temp("unitaries.npy"), unitaries)
    np.save(temp("conjugation_table.npy"), conjugation_table)
    np.save(temp("times_table.npy"), times_table)
    np.save(temp("cz_table.npy"), cz_table)

    with open(temp("by_name.json"), "wb") as f:
        json.dump(by_name, f)

