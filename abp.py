from clifford import *
from rightphase import RightPhase

"""
Porting Anders and Briegel to Python
"""

stab_rep = {None: "-", 0: "I", 1: "X", 2: "Y", 3:"Z"}

class Stabilizer(object):

    def __init__(self, graph):
        n = graph.nqubits
        self.paulis = [[None for i in range(n)] for j in range(n)]
        self.rowsigns = [None for i in range(n)]

        for i in range(n):
            self.rowsigns[i] = RightPhase(0)
            for j in range(n):
                if i == j:
                    self.paulis[i][j] = lco_x
                elif j in graph.vertices[i].neighbors:
                    self.paulis[i][j] = lco_z
                else:
                    self.paulis[i][j] = lco_id

                #self.conjugate(i, j, graph.vertices[j].vertex_operator)

    def conjugate(self, i, j, vertex_operator):
        self.rowsigns[j] = self.rowsigns[j] + \
            self.paulis[i][j].conjugate(vertex_operator)

    def __str__(self):
        return "\n".join(" ".join(stab_rep[x] for x in row) for row in self.paulis)


class Vertex(object):

    def __init__(self, index):
        self.index = index
        self.vertex_operator = lco_h
        self.neighbors = set()

    def edgelist(self):
        return [set((self.index, n)) for n in self.neighbors]

    def __str__(self):
        return "{}".format(", ".join(map(str, self.neighbors)))


class GraphRegister(object):

    def __init__(self, n):
        self.nqubits = n
        self.vertices = [Vertex(i) for i in xrange(n)]

    def add_edge(self, v1, v2):
        self.vertices[v1].neighbors.add(v2)
        self.vertices[v2].neighbors.add(v1)

    def del_edge(self, v1, v2):
        self.vertices[v1].neighbors.remove(v2)
        self.vertices[v2].neighbors.remove(v1)

    def toggle_edge(self, v1, v2):
        if v2 in self.vertices[v1].neighbors:
            self.del_edge(v1, v2)
        else:
            self.add_edge(v1, v2)

    def edgelist(self):
        return map(tuple, frozenset(frozenset((v.index, n))
                                    for v in self.vertices
                                    for n in v.neighbors))

    def __str__(self, ):
        return "\n".join(str(v) for v in self.vertices
                         if len(v.neighbors) > 0)

if __name__ == '__main__':
    g = GraphRegister(10)
    g.toggle_edge(0, 1)
    print g
