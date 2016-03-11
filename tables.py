"""
Enumerates the 24 elements of the local Clifford group, providing multiplication and conjugation tables
permutations = (id, ha, ph, ha*ph, ha*ph*ha, ha*ph*ha*ph) 
signs = (id, px, py, pz) 
unitaries = [p*s for p in permutations for s in signs]
"""

import numpy as np
from tqdm import tqdm
import qi
from functools import reduce
import cPickle

def cache_to_disk(file_name):
    """ A decorator to cache the output of a function to disk """
    def wrap(func):
        def modified(*args, **kwargs):
            try:
                output = cPickle.load(open(file_name, "r"))
            except (IOError, ValueError):
                output = func(*args, **kwargs)
                with open(file_name, "w") as f:
                    cPickle.dump(output, f)
            return output
        return modified
    return wrap


# TODO: make this more efficient / shorter
def find_up_to_phase(u):
    """ Find the index of a given u within a list of unitaries, up to a global phase  """
    for i, t in enumerate(unitaries):
        for phase in range(8):
            if np.allclose(t, np.exp(1j * phase * np.pi / 4.) * u):
                return i, phase
    raise IndexError


def compose_u(decomposition):
    """ Get the unitary representation of a particular decomposition """
    us = (elements[c] for c in decomposition)
    return np.matrix(reduce(np.dot, us), dtype=complex)


def name_of(vop):
    """ Get the formatted name of a VOP """
    return "%s" % get_name[vop] if vop in get_name else "VOP%d" % vop


@cache_to_disk("tables.cache")
def construct_tables():
    """ Constructs / caches multiplication and conjugation tables """
    by_name = {name: find_up_to_phase(u)[0] for name, u in qi.by_name.items()}
    get_name = {v:k for k, v in by_name.items()}
    conjugation_table = [find_up_to_phase(u.H)[0]
                         for i, u in enumerate(unitaries)]
    times_table = [[find_up_to_phase(u * v)[0] for v in unitaries]
                   for u in tqdm(unitaries)]
    cz_table = None
    return by_name, get_name, conjugation_table, times_table, cz_table


decompositions = ("xxxx", "xx", "zzxx", "zz", "zxx", "z", "zzz", "xxz",
     "xzx", "xzxxx", "xzzzx", "xxxzx", "xzz", "zzx", "xxx", "x",
     "zzzx", "xxzx", "zx", "zxxx", "xxxz", "xzzz", "xz", "xzxx")
elements = {"x": qi.sqx, "z": qi.msqz}
unitaries = [compose_u(d) for d in decompositions]
by_name, get_name, conjugation_table, times_table, cz_table = construct_tables()

