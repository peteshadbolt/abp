from abp import GraphState, VizClient
from abp.util import xyz
import numpy as np
import time
import itertools
import networkx as nx

threedee_unit_cell = (
     (( 0, 0, 0),    (0, 1, 0)),
     (( 0, 0, 0),    (1, 0, 0)),
     (( 1, 0, 0),    (1, 1, 0)),
     (( 0, 1, 0),    (1, 1, 0)),

     (( 0, 0, 1),    (0, 1, 1)),
     (( 0, 0, 1),    (1, 0, 1)),
     (( 1, 0, 1),    (1, 1, 1)),
     (( 0, 1, 1),    (1, 1, 1)),

     (( 0, 0, 0),    (0, 0, 1)),
     (( 0, 1, 0),    (0, 1, 1)),
     (( 1, 0, 0),    (1, 0, 1)),
     (( 1, 1, 0),    (1, 1, 1))
     )

def add_offset(vector, offset):
    """ Offset a vector in n-dimensional space """
    return tuple(v + o for v, o in zip(vector, offset))


def offset_unit_cell(unit_cell, offset):
    """ Offset a unit cell """
    return {(add_offset(a, offset), add_offset(b, offset)) for a, b in unit_cell}


def lattice(unit_cell, size):
    """ Generate a lattice from a unit cell """
    edges = set()
    for offset in itertools.product(*list(map(range, size))):
        edges |= offset_unit_cell(unit_cell, offset)

    nodes = set(itertools.chain(*edges))
    return nodes, edges

nodes, edges = lattice(threedee_unit_cell, (3, 3, 3))

psi = GraphState(nodes)

for a, b in edges:
    psi.act_cz(a, b)

v = VizClient()
v.update(psi)
