 #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Exposes a few basic QI operators
"""

import numpy as np
from scipy.linalg import sqrtm

# Operators
id = np.matrix(np.eye(2, dtype=complex))
px = np.matrix([[0, 1], [1, 0]], dtype=complex)
py = np.matrix([[0, -1j], [1j, 0]], dtype=complex)
pz = np.matrix([[1, 0], [0, -1]], dtype=complex)
ha = np.matrix([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
ph = np.matrix([[1, 0], [0, 1j]], dtype=complex)

sqy = sqrtm(1j * py)
msqy = np.matrix(sqrtm(-1j * py))
sqz = np.matrix(sqrtm(1j * pz))
msqz = np.matrix(sqrtm(-1j * pz))
sqx = np.matrix(sqrtm(1j * px))
msqx = np.matrix(sqrtm(-1j * px))
paulis = (px, py, pz)

# CZ gate
cz = np.matrix(np.eye(4), dtype=complex)
cz[3,3]=-1

# States
plus = np.matrix([[1],[1]], dtype=complex) / np.sqrt(2)
bond = cz * np.kron(plus, plus)
nobond = np.kron(plus, plus)

# Labelling stuff
common_us = id, px, py, pz, ha, ph, sqz, msqz, sqy, msqy, sqx, msqx
names = "identity", "px", "py", "pz", "hadamard", "phase", "sqz", "msqz", "sqy", "msqy", "sqx", "msqx"
by_name = dict(zip(names, common_us))
