# -*- coding: utf-8 -*-

"""
This module handles operations on the Clifford group. It makes extensive use of the lookup tables in ``abp.tables``. 
The code to generate those tables is included in this distribution as ``abp/build_tables.py``
This package emumerates and labels the single-qubit Clifford group, and provides methods for matrix multiplication and conjugation.
It also includes the look-up table for the CZ gate.

There are 24 members of the single-qubit Clifford group. You can refer to some of them by multiple names.
The complete set of aliases for single-qubit Cliffords is as follows:

    ======= =========================
    Index   Aliases
    ======= =========================
    0       ``IA, identity, identity_h``
    1       ``XA, px, px_h``
    2       ``YA, py, py_h``
    3       ``ZA, pz, pz_h``
    4       ``IB``
    5       ``XB, sqz, msqz_h, phase_h``
    6       ``YB, msqz, sqz_h, phase``
    7       ``ZB``
    8       ``IC``
    9       ``XC, msqy, sqy_h``
    10      ``YC, hadamard, hadamard_h``
    11      ``ZC, sqy, msqy_h``
    12      ``ID``
    13      ``XD``
    14      ``YD, sqx, msqx_h``
    15      ``ZD, msqx, sqx_h``
    16      ``IE``
    17      ``XE``
    18      ``YE``
    19      ``ZE``
    20      ``IF``
    21      ``XF``
    22      ``YF``
    23      ``ZF``
    ======= =========================

"""

from tables import *

# Aliases
identity = by_name["identity"]
hadamard = by_name["hadamard"]
px = by_name["px"]
py = by_name["py"]
pz = by_name["pz"]
msqx_h = by_name["msqx_h"]
sqz_h = by_name["sqz_h"]

def conjugate(operator, unitary):
    """ Returns transform * vop * transform^dagger and a phase in {+1, -1} """
    return measurement_table[operator, unitary]

def use_old_cz():
    """ Use the CZ lookup table from A&B's code, rather than our own. Useful for testing. """
    global cz_table
    from anders_cz import cz_table

def get_name(i):
    """ Get the name of this clifford """
    return "IXYZ"[i & 0x03] + "ABCDEF"[i / 4]

def human_name(i):
    """ Get the human-readable name of this clifford - slow """
    choices = sorted((key for key, value in by_name.items() if value == i), key=len)
    return choices[-1]

def is_diagonal(v):
    """ Checks if a VOP is diagonal or not """
    return v in {0, 3, 5, 6}


if __name__ == '__main__':
    from itertools import groupby

    for i in range(24):
        members = [key for key, value in by_name.items() if value == i and str(key)!=str(i)]
        members = sorted(members, key=len)
        print "* {}: {}".format(i, ", ".join(members))
            


