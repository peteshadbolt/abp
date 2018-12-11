# -*- coding: utf-8 -*-

"""
This module handles operations on the Clifford group. It makes extensive use of the lookup tables in ``abp.tables``.
The code to generate those tables is included in this distribution as ``abp/build_tables.py``
This package emumerates and labels the single-qubit Clifford group, and provides methods for matrix multiplication and conjugation.
It also includes the look-up table for the CZ gate.

There are 24 members of the single-qubit Clifford group. You can refer to some of them by multiple names.
The complete set of aliases for single-qubit Cliffords is as follows:

    === ====================== ===================== ====================== ======================= =========
    VOP Clifford               :math:`U^\\dagger XU`  :math:`U^\\dagger YU`   :math:`U^\\dagger ZU`     ABP Alias
                         
    === ====================== ===================== ====================== ======================= =========
    0   :math:`I`                   :math:`X`             :math:`Y`             :math:`Z`              ``IA, identity, identity_h``
    1   :math:`X`                   :math:`X`            :math:`-Y`            :math:`-Z`              ``XA, px, px_h``
    2   :math:`Y`                  :math:`-X`             :math:`Y`            :math:`-Z`              ``YA, py, py_h``
    3   :math:`Z`                  :math:`-X`            :math:`-Y`             :math:`Z`              ``ZA, pz, pz_h``
    4   :math:`XS`                 :math:`-Y`            :math:`-X`            :math:`-Z`              ``IB``
    5   :math:`S^\\dagger`         :math:`-Y`             :math:`X`             :math:`Z`              ``XB, sqz, msqz_h, phase_h``
    6   :math:`S`                   :math:`Y`            :math:`-X`             :math:`Z`              ``YB, msqz, sqz_h, phase``
    7   :math:`XS^\\dagger`         :math:`Y`             :math:`X`            :math:`-Z`              ``ZB``
    8   :math:`YH`                 :math:`-Z`            :math:`-Y`            :math:`-X`              ``IC``
    9   :math:`XH`                 :math:`-Z`             :math:`Y`             :math:`X`              ``XC, msqy, sqy_h``
    10  :math:`H`                   :math:`Z`            :math:`-Y`             :math:`X`              ``YC, hadamard, hadamard_h``
    11  :math:`ZH`                  :math:`Z`             :math:`Y`            :math:`-X`              ``ZC, sqy, msqy_h``
    12  :math:`S^\\dagger HS`      :math:`-X`            :math:`-Z`            :math:`-Y`              ``ID``
    13  :math:`SHS^\\dagger`       :math:`-X`             :math:`Z`             :math:`Y`              ``XD``
    14  :math:`SHS`                 :math:`X`            :math:`-Z`             :math:`Y`              ``YD, sqx, msqx_h``
    15  :math:`HSH`                 :math:`X`             :math:`Z`            :math:`-Y`              ``ZD, msqx, sqx_h``
    16  :math:`HS^\\dagger`         :math:`Y`             :math:`Z`             :math:`X`              ``IE``
    17  :math:`YHS^\\dagger`        :math:`Y`            :math:`-Z`            :math:`-X`              ``XE``
    18  :math:`YHS`                :math:`-Y`             :math:`Z`            :math:`-X`              ``YE``
    19  :math:`HS`                 :math:`-Y`            :math:`-Z`             :math:`X`              ``ZE``
    20  :math:`SH`                  :math:`Z`             :math:`X`             :math:`Y`              ``IF``
    21  :math:`S^\\dagger H`        :math:`Z`            :math:`-X`            :math:`-Y`              ``XF``
    22  :math:`XSH`                :math:`-Z`             :math:`X`            :math:`-Y`              ``YF``
    23  :math:`XS^\\dagger H`      :math:`-Z`            :math:`-X`             :math:`Y`              ``ZF``
    === ====================== ===================== ====================== ======================= =========

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
    from .anders_cz import cz_table

def get_name(i):
    """ Get the name of this clifford """
    return "IXYZ"[i & 0x03] + "ABCDEF"[i / 4]

def human_name(i):
    """ Get the human-readable name of this clifford - slow """
    choices = sorted((key for key, value in list(by_name.items()) if value == i), key=len)
    return choices[-1]

def is_diagonal(v):
    """ Checks if a VOP is diagonal or not """
    return v in {0, 3, 5, 6}


if __name__ == '__main__':
    from itertools import groupby

    for i in range(24):
        members = [key for key, value in list(by_name.items()) if value == i and str(key)!=str(i)]
        members = sorted(members, key=len)
        print("* {}: {}".format(i, ", ".join(members)))
            


