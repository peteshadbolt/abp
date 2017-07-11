from __future__ import absolute_import
from __future__ import print_function
from abp import GraphState
from tqdm import tqdm
import mock
from six.moves import range

REPEATS = 1000

def test_stabilizers_against_anders_and_briegel(n=10):
    """ Test that stabilizers are line-for-line equivalent """
    
    for i in tqdm(list(range(REPEATS)), "Stabilizer representation VS A&B"):
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
