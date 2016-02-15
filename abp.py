class Vertex(object):
    def __init__(self):
        self.neighbors = set()

    def __str__(self):
        return "v: {}".format(", ".join(map(str, self.neighbors)))

class GraphRegister(object):
    def __init__(self, n):
        self.vertices = [Vertex() for i in xrange(n)]

    def add_edge(self, v1, v2):
        self.vertices[v1].neighbors.add(v2)
        self.vertices[v2].neighbors.add(v1)


    def del_edge(self, v1, v2):
        self.vertices[v1].neighbors.remove(v2)
        self.vertices[v2].neighbors.remove(v1)

    def __str__(self, ):
        return "\n".join(str(v) for v in self.vertices)

if __name__ == '__main__':
    g = GraphRegister(10)
    g.add_edge(0,1)
    print g

