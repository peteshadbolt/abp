from abp import GraphState, clifford
from anders_briegel import graphsim
import numpy as np
from tqdm import tqdm
import dummy
import itertools as it

import networkx as nx


def all_simple_graphs(filename="tests/graph5.g6"):
    """ Generate all possible simple graphs """
    with open(filename) as f:
        for line in tqdm(f):
            yield nx.parse_graph6(line.strip())
    
def rotated(simple_graphs):
    for g in simple_graphs:
        for r in it.product(*[range(24)]*2):
            yield g, r


print len(list(rotated(all_simple_graphs())))


#N = 3
#m = {1: graphsim.lco_X, 2: graphsim.lco_Y, 3: graphsim.lco_Z}

#measurements = (3, 2, 1)
#outcomes = (0, 1)
#local_ops = it.combinations_with_replacement(range(24), N)
#edge_patterns = 

#print list(local_ops)

#print len(list(local_ops))
#print list(edge_patterns)

