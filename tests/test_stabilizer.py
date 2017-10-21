from abp import GraphState
from tqdm import tqdm
import mock

REPEATS = 1000

def test_stabilizers_against_anders_and_briegel(n=10):
    """ Test that stabilizers are line-for-line equivalent """
    
    for i in list(range(REPEATS)):
        c = mock.random_stabilizer_circuit(n)
        g = mock.AndersWrapper(list(range(n)))
        g.act_circuit(c)
        da = g.get_full_stabilizer().to_dictionary()

        g = mock.ABPWrapper(list(range(n)))
        g.act_circuit(c)
        db = g.to_stabilizer().to_dictionary()

        assert da == db

def test_stabilizer_access():
    g = GraphState(3)
    print(g.to_stabilizer()[0, 0])
