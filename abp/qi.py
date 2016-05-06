 #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Exposes a few basic QI operators
"""

import numpy as np
from scipy.linalg import sqrtm

def hermitian_conjugate(u):
    """ Shortcut to the Hermitian conjugate """
    return np.conjugate(np.transpose(u))

# Operators
id = np.array(np.eye(2, dtype=complex))
px = np.array([[0, 1], [1, 0]], dtype=complex)
py = np.array([[0, -1j], [1j, 0]], dtype=complex)
pz = np.array([[1, 0], [0, -1]], dtype=complex)
ha = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
ph = np.array([[1, 0], [0, 1j]], dtype=complex)

sqy = sqrtm(1j * py)
msqy = np.array(sqrtm(-1j * py))
sqz = np.array(sqrtm(1j * pz))
msqz = np.array(sqrtm(-1j * pz))
sqx = np.array(sqrtm(1j * px))
msqx = np.array(sqrtm(-1j * px))
paulis = (px, py, pz)

# CZ gate
cz = np.array(np.eye(4), dtype=complex)
cz[3,3]=-1

# States
plus = np.array([[1],[1]], dtype=complex) / np.sqrt(2)
bond = cz.dot(np.kron(plus, plus))
nobond = np.kron(plus, plus)

# Labelling stuff
common_us = id, px, py, pz, ha, ph, sqz, msqz, sqy, msqy, sqx, msqx
names = "identity", "px", "py", "pz", "hadamard", "phase", "sqz", "msqz", "sqy", "msqy", "sqx", "msqx"
by_name = dict(zip(names, common_us))
