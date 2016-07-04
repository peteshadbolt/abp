# -*- coding: utf-8 -*-

"""
This program generates and caches lookup tables, and handles the Clifford group.
It provides tables for Clifford group multiplication and conjugation,
as well as CZ and decompositions of the 2x2 Cliffords.
"""

import os, json, tempfile, json
from functools import reduce
import itertools as it
import numpy as np
from tqdm import tqdm
import qi

decompositions = ("xxxx", "xx", "zzxx", "zz", "zxx", "z", "zzz", "xxz",
                  "xzx", "xzxxx", "xzzzx", "xxxzx", "xzz", "zzx", "xxx", "x",
                  "zzzx", "xxzx", "zx", "zxxx", "xxxz", "xzzz", "xz", "xzxx")


def conjugate(operator, unitary):
    """ Returns transform * vop * transform^dagger and a phase in {+1, -1} """
    return measurement_table[operator, unitary]


def use_old_cz():
    """ Use the CZ table from A&B's code """
    global cz_table
    from anders_cz import cz_table


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
    a.update({get_name(i): i for i in range(24)})
    a.update({i: i for i in range(24)})
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


def get_measurement_entry(operator, unitary):
    """
    Any Clifford group unitary will map an operator A in {I, X, Y, Z}
    to an operator B in +-{I, X, Y, Z}. This finds that mapping.
    """
    matrices = ({"x": qi.msqx, "z": qi.sqz}[c]
                for c in decompositions[unitary])
    unitary = reduce(np.dot, matrices, np.eye(2, dtype=complex))
    operator = qi.operators[operator]
    new_operator = reduce(
        np.dot, (unitary, operator, qi.hermitian_conjugate(unitary)))

    for i, o in enumerate(qi.operators):
        if np.allclose(o, new_operator):
            return i, 1
        elif np.allclose(o, -new_operator):
            return i, -1

    raise IndexError


def get_measurement_table():
    """
    Compute a table of transform * operation * transform^dagger
    This is pretty unintelligible right now, we should probably compute the phase from unitaries instead
    """
    measurement_table = np.zeros((4, 24, 2), dtype=complex)
    for operator, unitary in it.product(range(4), range(24)):
        measurement_table[operator, unitary] = get_measurement_entry(
            operator, unitary)
    return measurement_table


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


def write_javascript_tables():
    """ Write the tables to javascript files for consumption in the browser """
    path = os.path.dirname(__file__)
    path = os.path.split(path)[0]
    with open(os.path.join(path, "static/scripts/tables.js"), "w") as f:
        f.write("var tables = {\n")
        f.write("\tdecompositions : {},\n"
                .format(json.dumps(decompositions)))
        f.write("\tconjugation_table : {},\n"
                .format(json.dumps(conjugation_table.tolist())))
        f.write("\ttimes_table : {},\n"
                .format(json.dumps(times_table.tolist())))
        f.write("\tcz_table : {},\n"
                .format(json.dumps(cz_table.tolist())))
        f.write("\tclifford : {}\n"
                .format(json.dumps(by_name)))
        f.write("};")


def temp(filename):
    """ Get a temporary path """
    # TODO: this STILL fucking fails sometimes. WHY
    tempdir = tempfile.gettempdir()
    return os.path.join(tempdir, filename)


def compute_everything():
    """ Compute all lookup tables """
    global unitaries, by_name, conjugation_table, times_table, cz_table, measurement_table
    unitaries = get_unitaries()
    by_name = get_by_name(unitaries)
    conjugation_table = get_conjugation_table(unitaries)
    times_table = get_times_table(unitaries)
    cz_table = get_cz_table(unitaries)
    measurement_table = get_measurement_table()


def save_to_disk():
    """ Save all tables to disk """
    global unitaries, by_name, conjugation_table, times_table, cz_table, measurement_table
    np.save(temp("unitaries.npy"), unitaries)
    np.save(temp("conjugation_table.npy"), conjugation_table)
    np.save(temp("times_table.npy"), times_table)
    np.save(temp("cz_table.npy"), cz_table)
    np.save(temp("measurement_table.npy"), measurement_table)
    write_javascript_tables()
    with open(temp("by_name.json"), "wb") as f:
        json.dump(by_name, f)


def load_from_disk():
    """ Load all the tables from disk """
    global unitaries, by_name, conjugation_table, times_table, cz_table, measurement_table
    unitaries = np.load(temp("unitaries.npy"))
    conjugation_table = np.load(temp("conjugation_table.npy"))
    times_table = np.load(temp("times_table.npy"))
    measurement_table = np.load(temp("measurement_table.npy"))
    cz_table = np.load(temp("cz_table.npy"))
    with open(temp("by_name.json")) as f:
        by_name = json.load(f)

def is_diagonal(v):
    """ TODO: remove this. Checks if a VOP is diagonal or not """
    return v in {0, 3, 5, 6}


if __name__ == "__main__":
    compute_everything()
    save_to_disk()
else:
    try:
        load_from_disk()
    except IOError:
        compute_everything()
        save_to_disk()
