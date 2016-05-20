from abp.viz import VisibleGraphState
from abp.util import xyz
import numpy as np
import time
import itertools

square_unit_cell = (
    ((0, 0), (0, 1)), ((0, 0), (1, 0)), ((1, 0), (1, 1)), ((0, 1), (1, 1)))
funny_unit_cell = (((0, 0), (0, 1)), ((0, 0), (1, 0)),
                   ((1, 0), (1, 1)), ((0, 1), (1, 1)), ((0, 0), (.5, .5)))


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

# s = VisibleGraphState()
nodes, edges = lattice(square_unit_cell, (4, 4))

psi = VisibleGraphState()
for node in nodes:
    psi.add_node(str(node), position=xyz(node[0], node[1]))
    psi.act_hadamard(str(node))

for edge in edges:
    psi.act_cz(str(edge[0]), str(edge[1]))

