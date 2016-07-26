from abp.fancy import GraphState as FGS
import abp
from abp.util import xyz

def linear_cluster(n):
    g = FGS(range(n), deterministic=False)
    g.act_circuit([(i, "hadamard") for i in range(n)])
    g.act_circuit([((i, i+1), "cz") for i in range(n-1)])
    return g 


def test_mercedes_example_1():
    """ Run an example provided by mercedes """

    g = linear_cluster(5)
    g.measure(2, "px", 1)
    g.measure(3, "px", 1)
    g.remove_vop(0, 1)
    g.remove_vop(1, 0)
    print g.node
    






if __name__ == '__main__':
    test_mercedes_example_1()
