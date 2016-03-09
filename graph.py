import networkx as nx
from matplotlib import pyplot as plt

vop_colors = ["red", "green", "blue"]

class Graph(object):

    def __init__(self, n):
        self.neighbours = [set() for i in xrange(n)]
        self.vops = [0 for i in xrange(n)]

    def add_edge(self, v1, v2):
        self.neighbours[v1].add(v2)
        self.neighbours[v2].add(v1)

    def del_edge(self, v1, v2):
        self.neighbours[v1].remove(v2)
        self.neighbours[v2].remove(v1)

    def has_edge(self, v1, v2):
        return v2 in self.neighbours[v1]

    def toggle_edge(self, v1, v2):
        if self.has_edge(v1, v2):
            self.del_edge(v1, v2)
        else:
            self.add_edge(v1, v2)


    def edgelist(self):
        edges = frozenset(frozenset((i, n))
                for i, v in enumerate(self.neighbours)
                for n in v)
        return [tuple(e) for e in edges]

    def draw(self, filename="out.pdf", ns=500):
        g = nx.from_edgelist(self.edgelist())
        pos = nx.spring_layout(g)
        colors = [vop_colors[vop] for vop in self.vops]
        nx.draw_networkx_nodes(g, pos, node_color="white", node_size=ns)
        nx.draw_networkx_nodes(g, pos, node_color=colors, node_size=ns, alpha=.4)
        nx.draw_networkx_labels(g, pos)
        nx.draw_networkx_edges(g, pos)

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
