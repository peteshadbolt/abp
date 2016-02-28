 #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Exposes a few basic QI operators
"""

import numpy as np
from scipy.linalg import sqrtm

id = np.matrix(np.eye(2, dtype=complex))
px = np.matrix([[0, 1], [1, 0]], dtype=complex)
py = np.matrix([[0, -1j], [1j, 0]], dtype=complex)
pz = np.matrix([[1, 0], [0, -1]], dtype=complex)
ha = np.matrix([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
ph = np.matrix([[1, 0], [0, 1j]], dtype=complex)

sqy = sqrtm(1j * py)
msqy = sqrtm(-1j * py)
sqz = sqrtm(1j * pz)
msqz = sqrtm(-1j * pz)
sqx = sqrtm(1j * px)
msqx = sqrtm(-1j * px)
paulis = (px, py, pz)
