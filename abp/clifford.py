# -*- coding: utf-8 -*-

"""
This program generates and caches lookup tables, and handles the Clifford group.
It provides tables for Clifford group multiplication and conjugation,
as well as CZ and decompositions of the 2x2 Cliffords.
"""

from tables import *

def conjugate(operator, unitary):
    """ Returns transform * vop * transform^dagger and a phase in {+1, -1} """
    return measurement_table[operator, unitary]

def use_old_cz():
    """ Use the CZ table from A&B's code """
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
    """ TODO: remove this. Checks if a VOP is diagonal or not """
    return v in {0, 3, 5, 6}


