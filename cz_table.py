import qi
import numpy as np
import tables
from tqdm import tqdm
import itertools as it

def get_krontable():
    table = np.zeros((24,24,4,4), dtype=complex)
    for i, j in it.product(range(24), range(24)):
        u1 = tables.unitaries[i]
        u2 = tables.unitaries[j]
        table[i, j, :, :] = np.kron(u1, u2)
    return table

def find(bond, c1, c2, z, krontable):
    # Figure out the target state
    state = qi.bond if bond else qi.nobond
    target = qi.cz * krontable[c1, c2] * state

    # Choose the sets to search over
    s1 = z if c1 in z else xrange(24)
    s2 = z if c2 in z else xrange(24)

    for bond, c1p, c2p in it.product([0,1], s1, s2):
        state = qi.bond if bond else qi.nobond
        trial = krontable[c1p, c2p] * state
        for phase in range(8):
            if np.allclose(target, np.exp(1j * phase * np.pi / 4.) * trial):
                return bond, c1p, c2p

    raise IndexError


z = [tables.find(u, tables.unitaries) for u in qi.id, qi.px, qi.pz, qi.ph, qi.ph.H]
krontable = get_krontable()

cz_table = np.zeros((2, 24, 24, 3))
for bond, c1, c2 in tqdm(list(it.product([0,1], range(24), range(24)))):
    cz_table[bond, c1, c2] = find(bond, c1, c2, z, krontable)

np.save("cz_table.npy", cz_table)

