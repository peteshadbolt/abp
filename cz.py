from matplotlib import pyplot as plt
from graph import *
from viz import draw

def local_complementation(g, vops, a):
    for i in g[a]:
        for j in g[a]:
            if i<j:
                toggle_edge(g, i, j)

if __name__ == '__main__':
    g, vops = graph(10)
    add_edge(g, 0, 1)
    add_edge(g, 1, 3)
    add_edge(g, 3, 2)
    add_edge(g, 3, 0)
    add_edge(g, 2, 0)
    add_edge(g, 0, 5)
    vops[0]=1
    draw(g, vops)
    plt.clf()
    local_complementation(g, vops, 0)
    draw(g, vops, "out2.pdf")

