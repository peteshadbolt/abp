from abp import GraphState, VizClient
from abp.util import xyz
import numpy as np
import time
import itertools
import networkx as nx

raussendorf_unit_cell = (
     ((1, 0, 0), (1, 1, 0)), ((0, 1, 0), (1, 1, 0)),
     ((1, 2, 0), (1, 1, 0)), ((2, 1, 0), (1, 1, 0)),
     ((1, 2, 2), (1, 1, 2)), ((0, 1, 2), (1, 1, 2)),
     ((1, 0, 2), (1, 1, 2)), ((2, 1, 2), (1, 1, 2)),
     ((0, 1, 0), (0, 1, 1)), ((0, 0, 1), (0, 1, 1)),
     ((0, 1, 2), (0, 1, 1)), ((0, 2, 1), (0, 1, 1)),
     ((2, 1, 0), (2, 1, 1)), ((2, 0, 1), (2, 1, 1)),
     ((2, 1, 2), (2, 1, 1)), ((2, 2, 1), (2, 1, 1)),
     ((1, 0, 0), (1, 0, 1)), ((0, 0, 1), (1, 0, 1)),
     ((1, 0, 2), (1, 0, 1)), ((2, 0, 1), (1, 0, 1)),  
     ((1, 2, 0), (1, 2, 1)), ((0, 2, 1), (1, 2, 1)),
     ((1, 2, 2), (1, 2, 1)), ((2, 2, 1), (1, 2, 1)))


def add_offset(vector, offset):
    """ Offset a vector in n-dimensional space """
    return tuple(v + o*2 for v, o in zip(vector, offset))


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

nodes, edges = lattice(raussendorf_unit_cell, (2, 2, 3 ))

psi = GraphState()
for node in nodes:
    x, y, z = node
    color = "red" if (x+y+z) % 2 > 0  else "black"
    print color
    psi.add_qubit(node, position=xyz(*node), color=color)
    psi.act_hadamard(node)

for edge in edges:
    psi.act_cz(edge[0], edge[1])

v = VizClient()
v.update(psi)

