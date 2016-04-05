import qi
import numpy as np
import tables
import tqdm

# TODO: ensure that Constraint 1 is met. i.e. 
# if C1 is in Z, choose C1' such that it is in Z

bond = qi.cz * np.kron(qi.plus, qi.plus)
no_bond = np.kron(qi.plus, qi.plus)

for u in tables.unitaries:
    psi = qi.cz*np.kron(u, qi.ha)*bond

    for bb in bond, no_bond:
        for a in tables.unitaries:
            for b in tables.unitaries:
                if np.allclose(np.kron(a, b)*bb, psi):
                    print "match"

