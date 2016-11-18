"""
This program computes lookup tables and stores them as tables.py and tables.js
# TODO: clifford naming discrepancy
"""

import numpy as np
from tqdm import tqdm
import itertools as it
from functools import reduce
from os.path import dirname, join, split
import json
import qi, clifford


DECOMPOSITIONS = (
    "xxxx", "xx", "zzxx", "zz", "zxx", "z", "zzz", "xxz", "xzx", "xzxxx", "xzzzx",
                  "xxxzx", "xzz", "zzx", "xxx", "x", "zzzx", "xxzx", "zx", "zxxx", "xxxz", "xzzz", "xz", "xzxx")


PY_TEMPLATE = """\
import numpy as np

# Define lookup tables
ir2 = 1/np.sqrt(2)
decompositions = {decompositions}
conjugation_table = np.array({conjugation_table}, dtype=int)
times_table = np.array({times_table}, dtype=int)
cz_table = np.array({cz_table}, dtype=int)
by_name = {by_name}
measurement_table = np.array({measurement_table}, dtype=int)
unitaries_real = np.array({unitaries_real}, dtype=complex)
unitaries_imag = np.array({unitaries_imag}, dtype=complex)

# Reconstruct
unitaries = unitaries_real + 1j*unitaries_imag
"""


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
    return [compose_u(d) for d in DECOMPOSITIONS]


def get_by_name(unitaries, conjugation_table):
    """ Get a lookup table of cliffords by name """
    a = {name: find_clifford(u, unitaries)
         for name, u in qi.by_name.items()}
    a.update({key + "_h": conjugation_table[value]
              for key, value in a.items()})
    a.update({clifford.get_name(i): i for i in range(24)})
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
                for c in DECOMPOSITIONS[unitary])
    unitary = reduce(np.dot, matrices, np.eye(2, dtype=complex))
    operator = qi.operators[operator]
    new_operator = reduce(np.dot,
                          (unitary, operator, qi.hermitian_conjugate(unitary)))

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
    measurement_table = np.zeros((4, 24, 2), dtype=int)
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


def get_display_table(unitaries):
    """ Used to display VOPs in a human readable style """
    for u in unitaries:
        c = qi.CircuitModel(1)
        c.act_local_rotation(0, u)
        state = c.state.round(2)
        print "{:.2f}, {:.2f}".format(state[0][0], state[1][0])


def compute_everything():
    """ Compute all lookup tables """
    unitaries = get_unitaries()
    conjugation_table = get_conjugation_table(unitaries)
    return {"decompositions": DECOMPOSITIONS,
            "unitaries": unitaries,
            "by_name": get_by_name(unitaries, conjugation_table),
            "conjugation_table": conjugation_table,
            "times_table": get_times_table(unitaries),
            "cz_table": get_cz_table(unitaries),
            "measurement_table": get_measurement_table()}


def human_readable(data):
    """ Format the data """
    unitaries = np.array(data["unitaries"])
    return {"decompositions": json.dumps(DECOMPOSITIONS),
            "unitaries_real": json.dumps(unitaries.real.round(5).tolist()).replace("0.70711", "ir2"),
            "unitaries_imag": json.dumps(unitaries.imag.round(5).tolist()).replace("0.70711", "ir2"),
            "conjugation_table": json.dumps(data["conjugation_table"].tolist()),
            "times_table": json.dumps(data["times_table"].tolist()),
            "cz_table": json.dumps(data["cz_table"].tolist()),
            "by_name": json.dumps(data["by_name"]),
            "measurement_table": json.dumps(data["measurement_table"].tolist())}


def write_python(data):
    """ Write the tables to a python module """
    path = join(dirname(__file__), "tables.py")
    content = PY_TEMPLATE.format(**data)
    with open(path, "w") as f:
        f.write(content)


if __name__ == '__main__':
    get_display_table(get_unitaries())
    data = compute_everything()
    data = human_readable(data)
    write_python(data)
