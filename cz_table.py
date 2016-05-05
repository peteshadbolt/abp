import qi
import numpy as np
import tables
import tqdm

# TODO: ensure that Constraint 1 is met. i.e. 
# if C1 is in Z, choose C1' such that it is in Z

table1 = []
table2 = []

bond = qi.cz * np.kron(qi.plus, qi.plus)
no_bond = np.kron(qi.plus, qi.plus)

def find(thing, table):
    for index, trial in enumerate(table):
        for qq in range(16):
            if np.allclose(thing, np.exp(2j*np.pi*qq/16.) * trial):
                yield index

for state in bond, no_bond:
    for a in tables.unitaries:
        for b in tables.unitaries:
            state = np.kron(a, b) * state
            table1.append(state)
            table2.append(qi.cz*state)

for index, thing in enumerate(table2):
    print "{} -> {}".format(index, list(find(thing, table1)))



