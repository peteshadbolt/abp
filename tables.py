"""
Enumerates the 24 elements of the local Clifford group, providing multiplication and conjugation tables
permutations = (id, ha, ph, ha*ph, ha*ph*ha, ha*ph*ha*ph) 
signs = (id, px, py, pz) 
unitaries = [p*s for p in permutations for s in signs]
"""

import numpy as np
from tqdm import tqdm
import os
from functools import reduce
import cPickle
import qi

# TODO: make this more efficient / shorter
def find(needle, haystack):
    """ Find the index of a given u within a list of unitaries, up to a global phase  """
    for i, t in enumerate(haystack):
        for phase in range(8):
            if np.allclose(t, np.exp(1j * phase * np.pi / 4.) * needle):
                return i
    raise IndexError


def compose_u(decomposition):
    """ Get the unitary representation of a particular decomposition """
    us = ({"x": qi.sqx, "z": qi.msqz}[c] for c in decomposition)
    return np.matrix(reduce(np.dot, us), dtype=complex)


def name_of(vop):
    """ Get the formatted name of a VOP """
    return "%s" % get_name[vop] if vop in get_name else "VOP%d" % vop


def construct_tables(filename="tables.cache"):
    """ Constructs / caches multiplication and conjugation tables """
    if os.path.exists(filename):
        return cPickle.load(open(filename, "r"))

    by_name = {name: find(u, unitaries) for name, u in qi.by_name.items()}
    get_name = {v:k for k, v in by_name.items()}
    conjugation_table = [find(u.H, unitaries)
                         for i, u in enumerate(unitaries)]
    times_table = [[find(u * v, unitaries) for v in unitaries]
                   for u in tqdm(unitaries)]
    cz_table = None
    output = by_name, get_name, conjugation_table, times_table, cz_table

    with open(filename, "w") as f:
        cPickle.dump(output, f)
    return output

decompositions = ("xxxx", "xx", "zzxx", "zz", "zxx", "z", "zzz", "xxz",
     "xzx", "xzxxx", "xzzzx", "xxxzx", "xzz", "zzx", "xxx", "x",
     "zzzx", "xxzx", "zx", "zxxx", "xxxz", "xzzz", "xz", "xzxx")
unitaries = [compose_u(d) for d in decompositions]
by_name, get_name, conjugation_table, times_table, cz_table = construct_tables()
