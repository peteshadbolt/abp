from abp import GraphState, VizClient
from abp.util import xyz
import itertools

def grid_2d(width, height):
    """ Make a 2D grid """
    psi = GraphState()
    grid = list(itertools.product(range(width), range(height)))

    for x, y in grid:
        psi.add_qubit((x, y), position=xyz(x, y, 0), vop=0)

    for x, y in grid:
        if x<width-1: psi.act_cz((x, y), (x+1, y))
        if y<height-1: psi.act_cz((x, y), (x, y+1))

    return psi


if __name__ == '__main__':
    psi = grid_2d(5, 5)
    v = VizClient()
    v.update(psi)

