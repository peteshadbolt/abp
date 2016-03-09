from graph import Graph
from matplotlib import pyplot as plt

class GraphState(Graph):

    def __init__(self, n):
        Graph.__init__(self, n)

    def local_complementation(self, a):
        for i in self.neighbours[a]:
            for j in self.neighbours[a]:
                if i<j:
                    self.toggle_edge(i, j)

if __name__ == '__main__':
    g = GraphState(10)
    g.add_edge(0, 1)
    g.add_edge(1, 3)
    g.add_edge(3, 2)
    g.add_edge(3, 0)
    g.add_edge(2, 0)
    g.add_edge(0, 5)
    g.vops[0]=1
    g.draw()

    plt.clf()
    g.local_complementation(0)
    g.draw("out2.pdf")

