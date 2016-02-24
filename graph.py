import networkx as nx
from matplotlib import pyplot as plt
from vops import *

class Graph(object):

    def __init__(self, n):
        self.vertices = [set() for i in xrange(n)]
        self.vops = [hadamard for i in xrange(n)]

    def add_edge(self, v1, v2):
        self.vertices[v1].add(v2)
        self.vertices[v2].add(v1)

    def del_edge(self, v1, v2):
        self.vertices[v1].remove(v2)
        self.vertices[v2].remove(v1)

    def edgelist(self):
        edges = frozenset(frozenset((i, n))
                for i, v in enumerate(self.vertices)
                for n in v)
        return [tuple(e) for e in edges]

    def draw(self, filename="out.pdf"):
        g = nx.from_edgelist(self.edgelist())
        pos = nx.spring_layout(g)
        nx.draw_networkx_nodes(g, pos, node_color="white", node_size=1000)
        nx.draw_networkx_labels(g, pos)
        nx.draw_networkx_edges(g, pos)
        for i, vop in enumerate(self.vops):
            if not i in pos: continue
            x, y = pos[i]
            plt.text(x, y+0.1, vops[vop], ha="center")

        plt.axis('off')
        plt.savefig(filename)

if __name__ == '__main__':
    g = Graph(10)
    g.add_edge(0, 1)
    g.add_edge(1, 3)
    g.add_edge(3, 2)
    g.add_edge(3, 0)
    g.add_edge(2, 0)
    print g.edgelist()

    g.draw()
