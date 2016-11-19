from abp.fancy import GraphState
from abp.util import xyz
import numpy as np
import time
import itertools

threedee_unit_cell = (
     (( 0, 0, 0),    (0, 1, 0)),
     (( 0, 0, 0),    (1, 0, 0)),
     (( 1, 0, 0),    (1, 1, 0)),
     (( 0, 1, 0),    (1, 1, 0)))

def add_offset(vector, offset):
    """ Offset a vector in n-dimensional space """
    return tuple(v + o for v, o in zip(vector, offset))


def offset_unit_cell(unit_cell, offset):
    """ Offset a unit cell """
    return {(add_offset(a, offset), add_offset(b, offset)) for a, b in unit_cell}


def lattice(unit_cell, size):
    """ Generate a lattice from a unit cell """
    edges = set()
    for offset in itertools.product(*map(range, size)):
        edges |= offset_unit_cell(unit_cell, offset)

    nodes = set(itertools.chain(*edges))
    return nodes, edges

nodes, edges = lattice(threedee_unit_cell, (4, 4, 4))

while True:
    psi = GraphState()
    for node in nodes:
        psi.add_qubit(str(node), position=xyz(node[0], node[1], node[2]), vop="identity")
    psi.update(0.1)

    for edge in edges:
        psi.act_cz(str(edge[0]), str(edge[1]))
    psi.update(0.1)


