 #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Exposes a few basic QI operators
"""

import numpy as np
from scipy.linalg import sqrtm
import itertools as it

def hermitian_conjugate(u):
    """ Shortcut to the Hermitian conjugate """
    return np.conjugate(np.transpose(u))

# Constants 
ir2 = 1/np.sqrt(2)
# Operators
id = np.array(np.eye(2, dtype=complex))
px = np.array([[0, 1], [1, 0]], dtype=complex)
py = np.array([[0, -1j], [1j, 0]], dtype=complex)
pz = np.array([[1, 0], [0, -1]], dtype=complex)
ha = np.array([[1, 1], [1, -1]], dtype=complex) * ir2
ph = np.array([[1, 0], [0, 1j]], dtype=complex)
t = np.array([[1, 0], [0, np.exp(1j*np.pi/4)]], dtype=complex)

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

paulis = px, py, pz

class CircuitModel(object):
    def __init__(self, nqubits):
        self.nqubits = nqubits
        self.d = 2**nqubits
        self.state = np.zeros((self.d, 1), dtype=complex)
        self.state[0, 0]=1

    def act_cz(self, control, target):
        """ Act a CU somewhere """
        control = 1 << control
        target = 1 << target
        for i in xrange(self.d):
            if (i & control) and (i & target):
                self.state[i, 0] *= -1

    def act_hadamard(self, qubit):
        """ Act a hadamard somewhere """
        where = 1 << qubit
        output = np.zeros((self.d, 1), dtype=complex)
        for i, v in enumerate(self.state):
            q = i & where > 0
            output[i] += v*ha[q, q]
            output[i ^ where] += v*ha[not q, q]
        self.state = output


    def act_local_rotation(self, qubit, u):
        """ Act a local unitary somwhere """
        where = 1 << qubit
        output = np.zeros((self.d, 1), dtype=complex)
        for i, v in enumerate(self.state):
            q = i & where > 0
            output[i] += v*u[q, q]
            output[i ^ where] += v*u[not q, q]
        self.state = output


    def __str__(self):
        s = ""
        for i in range(self.d):
            label = bin(i)[2:].rjust(self.nqubits, "0")
            if abs(self.state[i, 0])>0.00001:
                s += "|{}>: {}\n".format(label, self.state[i, 0].round(3))
        return s

