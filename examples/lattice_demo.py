from abp.viz import VisibleGraphState
import numpy as np
import time
import itertools

square_unit_cell = (((0, 0), (0, 1)), ((0, 0), (1, 0)), ((1, 0), (1, 1)), ((0, 1), (1, 1)))
funny_unit_cell = (((0, 0), (0, 1)), ((0, 0), (1, 0)), ((1, 0), (1, 1)), ((0, 1), (1, 1)), ((0, 0), (.5, .5)))

def add_offset(vector, offset):
    """ Offset a vector in n-dimensional space """
    return tuple(v+o for v, o in zip(vector, offset))

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

#s = VisibleGraphState()
nodes, edges = lattice(funny_unit_cell, (10, 10))

psi = VisibleGraphState()
for node in nodes:
    pos = {"x": node[0], "y": node[1], "z": 0}
    psi.add_node(str(node), meta={"position":pos})

for edge in edges:
    psi.add_edge(str(edge[0]), str(edge[1]))


