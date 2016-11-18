#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Exposes a few basic QI operators
And a circuit-model simulator
"""

import numpy as np
import itertools as it
from fractions import Fraction

def hermitian_conjugate(u):
    """ Shortcut to the Hermitian conjugate """
    return np.conjugate(np.transpose(u))

# Constants
ir2 = 1 / np.sqrt(2)
# Operators
id = np.array(np.eye(2, dtype=complex))
px = np.array([[0, 1], [1, 0]], dtype=complex)
py = np.array([[0, -1j], [1j, 0]], dtype=complex)
pz = np.array([[1, 0], [0, -1]], dtype=complex)
ha = hadamard = np.array([[1, 1], [1, -1]], dtype=complex) * ir2
ph = np.array([[1, 0], [0, 1j]], dtype=complex)
t = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)

sqx = np.array(
    [[1. + 0.j, -0. + 1.j], [-0. + 1.j, 1. - 0.j]], dtype=complex) * ir2
msqx = np.array(
    [[1. + 0.j, 0. - 1.j], [0. - 1.j, 1. - 0.j]], dtype=complex) * ir2
sqy = np.array(
    [[1. + 0.j, 1. + 0.j], [-1. - 0.j, 1. - 0.j]], dtype=complex) * ir2
msqy = np.array(
    [[1. + 0.j, -1. - 0.j], [1. + 0.j, 1. - 0.j]], dtype=complex) * ir2
sqz = np.array(
    [[1. + 1.j, 0. + 0.j], [0. + 0.j, 1. - 1.j]], dtype=complex) * ir2
msqz = np.array(
    [[1. - 1.j, 0. + 0.j], [0. + 0.j, 1. + 1.j]], dtype=complex) * ir2

# CZ gate
cz = np.array(np.eye(4), dtype=complex)
cz[3, 3] = -1

# States
zero = np.array([[1], [0]], dtype=complex)
one = np.array([[0], [1]], dtype=complex)
plus = np.array([[1], [1]], dtype=complex) / np.sqrt(2)
bond = cz.dot(np.kron(plus, plus))
nobond = np.kron(plus, plus)

# Labelling stuff
common_us = id, px, py, pz, ha, ph, sqz, msqz, sqy, msqy, sqx, msqx
names = "identity", "px", "py", "pz", "hadamard", "phase", "sqz", "msqz", "sqy", "msqy", "sqx", "msqx"
by_name = dict(zip(names, common_us))

paulis = px, py, pz
operators = id, px, py, pz


def normalize_global_phase(m):
    """ Normalize the global phase of a matrix """
    v = (x for x in m.flatten() if np.abs(x) > 0.001).next()
    phase = np.arctan2(v.imag, v.real) % np.pi
    rot = np.exp(-1j * phase)
    return rot * m if rot * v > 0 else -rot * m


class CircuitModel(object):

    def __init__(self, nqubits):
        self.nqubits = nqubits
        self.d = 2 ** nqubits
        self.state = np.zeros((self.d, 1), dtype=complex)
        self.state[0, 0] = 1

    def act_cz(self, control, target):
        """ Act a CU somewhere. """
        control = 1 << control
        target = 1 << target
        for i in xrange(self.d):
            if (i & control) and (i & target):
                self.state[i, 0] *= -1

    def act_cnot(self, control, target):
        """ Act a CNOT. """
        self.act_hadamard(target)
        self.act_cz(control, target)
        self.act_hadamard(target)

    def act_hadamard(self, qubit):
        """ Act a hadamard somewhere. """
        where = 1 << qubit
        output = np.zeros((self.d, 1), dtype=complex)
        for i, v in enumerate(self.state):
            q = int(i & where > 0)
            output[i] += v * ha[q, q]
            output[i ^ where] += v * ha[int(not q), q]
        self.state = output

    def act_local_rotation(self, qubit, u):
        """ Act a local unitary somwhere. """
        where = 1 << qubit
        output = np.zeros((self.d, 1), dtype=complex)
        for i, v in enumerate(self.state):
            q = int(i & where > 0)
            output[i] += v * u[q, q]
            output[i ^ where] += v * u[int(not q), q]
        self.state = output

    def act_circuit(self, circuit):
        """ Act a sequence of gates. """
        for node, operation in circuit:
            if operation == "cz":
                self.act_cz(*node)
            else:
                self.act_local_rotation(node, operation)

    def __eq__(self, other):
        """ Check whether two quantum states are the same or not,
            up to a global phase. """
        a = normalize_global_phase(self.state)
        b = normalize_global_phase(other.state)
        return np.allclose(a, b)

    def __setitem__(self, key, value):
        """ Set a matrix element """
        self.state[key] = value

    def __getitem__(self, key):
        """ Get a matrix element """
        return self.state[key]

    def __str__(self):
        s = ""
        for i in range(self.d):
            label = bin(i)[2:].rjust(self.nqubits, "0")[::-1]
            if abs(self.state[i, 0]) > 0.00001:
                term = self.state[i, 0]
                real_sign = " " if term.real>=0 else "-"
                real_frac = Fraction(str(term.real**2)).limit_denominator()
                imag_sign = "+" if term.imag>=0 else "-"
                imag_frac = Fraction(str(term.imag**2)).limit_denominator()
                s += "|{}❭: \t{}√{}\t{} i √{}\n".format(
                        label, real_sign, real_frac, imag_sign, imag_frac)
        return s
