import numpy as np
from tqdm import tqdm
import os
from qi import *
import cPickle

def find_up_to_phase(u):
    """ Find the index of a given u within a list of unitaries, up to a global phase  """
    global unitaries
    for i, t in enumerate(unitaries):
        for phase in range(8):
            if np.allclose(t, np.exp(1j*phase*np.pi/4.)*u):
                return i, phase
    raise IndexError


def compose_u(decomposition):
    """ Get the unitary representation of a particular decomposition """
    us = (elements[c] for c in decomposition)
    return np.matrix(reduce(np.dot, us), dtype=complex)


def construct_tables():
    """ Constructs multiplication and conjugation tables """
    conjugation_table = [find_up_to_phase(u.H)[0] for i, u in enumerate(unitaries)]
    times_table = [[find_up_to_phase(u*v)[0] for v in unitaries] 
            for u in tqdm(unitaries, "Building times-table")]
    with open("tables.pkl", "w") as f:
        cPickle.dump((conjugation_table, times_table), f)


decompositions = \
("xxxx", "xx", "zzxx", "zz", "zxx", "z", "zzz", "xxz",
"xzx", "xzxxx", "xzzzx", "xxxzx", "xzz", "zzx", "xxx", "x",
"zzzx", "xxzx", "zx", "zxxx", "xxxz", "xzzz", "xz", "xzxx")
elements = {"x": sqx, "z": msqz}
unitaries = [compose_u(d) for d in decompositions]

# Build / reload lookup tables
if not os.path.exists("tables.pkl"):
    construct_tables()

if __name__ == '__main__':
    pass
