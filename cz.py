from graph import *
import viz
import itertools as it
import clifford

#def cphase(a, b):
    #""" Act a controlled-phase gate on two qubits """
    #if g

def remove_vop(g, vops, a, avoid):
    """ Reduces VOP[a] to the identity, avoiding (if possible) the use of vertex b as a swapping partner """
    other_neighbours = g[a] - {avoid}
    c = avoid if len(other_neighbours) == 0 else other_neighbours.pop()
    d = clifford.decompositions[vops[a]]
    for v in reversed(d):
        target = a if v == "x" else c
        local_complementation(g, vops, target)


def local_complementation(g, vops, v):
    """ As defined in LISTING 1 of Anders & Briegel """
    for i, j in it.combinations(g[v], 2):
        toggle_edge(g, i, j)

    # Update VOPs
    vops[v] = clifford.times_table[vops[v]][clifford.by_name["sqx"]]
    for i in g[v]:
        vops[i] = clifford.times_table[vops[i]][clifford.by_name["msqz"]]


if __name__ == '__main__':
    g, vops = graph()
    add_edge(g, 0, 1)
    add_edge(g, 1, 2)
    add_edge(g, 0, 2)
    add_edge(g, 0, 3)
    add_edge(g, 6, 7)

    pos = viz.draw(g, vops, "out.pdf")
    remove_vop(g, vops, 0, 1)
    viz.draw(g, vops, "out2.pdf", pos)
