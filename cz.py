from graph import *
import viz
import itertools as it
import clifford

def cphase(g, vops, a, b):
    """ Act a controlled-phase gate on two qubits """
    if g[a]-{b}: remove_vop(g, vops, a, b)
    if g[b]-{a}: remove_vop(g, vops, b, a)
    if g[a]-{b}: remove_vop(g, vops, a, b)
    edge = has_edge(g, a, b)
    new_edge, vops[a], vops[b] = cphase_table[edge, vops[a], vops[b]]
    if new_edge != edge:
        toggle_edge(g, a, b)
    

def remove_vop(g, vops, a, avoid):
    """ Reduces VOP[a] to the identity, avoiding (if possible) the use of vertex b as a swapping partner """
    others = g[a] - {avoid}
    swap_qubit = others.pop() if others else avoid
    for v in reversed(clifford.decompositions[vops[a]]):
        local_complementation(g, vops, a if v == "x" else swap_qubit)


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
    remove_vop(g, vops, 1, 2)
    cphase(g, vops, 0, 1)
    viz.draw(g, vops, "out2.pdf", pos)
