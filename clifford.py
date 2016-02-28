 #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Generates and enumerates the 24 elements of the local Clifford group
Following the prescription of Anders (thesis pg. 26):
> Table 2.1: The 24 elements of the local Clifford group. The row index (here called the “sign symbol”) shows how the operator
> U permutes the Pauli operators σ = X, Y, Z under the conjugation σ = ±UσU† . The column index (the “permutation
> symbol”) indicates the sign obtained under the conjugation: For operators U in the I column it is the sign of the permutation
> (indicated on the left). For elements in the X, Y and Z columns, it is this sign only if the conjugated Pauli operator is the one
> indicated by the column header and the opposite sign otherwise.
"""

import numpy as np
from qi import *
from tqdm import tqdm
import cPickle,os

def find_up_to_phase(u):
    """ Find the index of a given u within a list of unitaries, up to a global phase  """
    global unitaries
    for i, t in enumerate(unitaries):
        for phase in range(8):
            if np.allclose(t, np.exp(1j*phase*np.pi/4.)*u):
                return i, phase
    raise IndexError

def construct_tables():
    """ Constructs multiplication and conjugation tables """
    conjugation_table = [find_up_to_phase(u.H)[0] for i, u in enumerate(unitaries)]
    times_table = [[find_up_to_phase(u*v)[0] for v in unitaries] 
            for u in tqdm(unitaries, "Building times-table")]
    with open("tables.pkl", "w") as f:
        cPickle.dump((conjugation_table, times_table), f)

permutations = (id, ha, ph, ha*ph, ha*ph*ha, ha*ph*ha*ph)
signs = (id, px, py, pz)
unitaries = [p*s for p in permutations for s in signs]

# Build / reload lookup tables
if not os.path.exists("tables.pkl"):
    construct_tables()

with open("tables.pkl") as f:
    conjugation_table, times_table = cPickle.load(f)


