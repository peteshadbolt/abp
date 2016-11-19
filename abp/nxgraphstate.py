import networkx as nx
import numpy as np
import graphstate
import clifford
import util

class NXGraphState(graphstate.GraphState, nx.Graph):
    """ This is GraphState with NetworkX-like abilities """
    def __init__(self, *args, **kwargs):
        graphstate.GraphState.__init__(self, *args, **kwargs)

    def layout(self):
        """ Automatically lay out the graph """
        pos = nx.spring_layout(self, dim=3, scale=np.sqrt(self.order()))
        middle = np.average(pos.values(), axis=0)
        pos = {key: value - middle for key, value in pos.items()}
        for key, (x, y, z) in pos.items():
            self.node[key]["position"] = util.xyz(x, y, z)

