from abp import GraphState
from tqdm import tqdm
import mock

REPEATS = 1000

def test_stabilizers_against_anders_and_briegel(n=10):
    """ Test that stabilizers are line-for-line equivalent """
    
    for i in tqdm(range(REPEATS), "Stabilizer representation VS A&B"):
        c = mock.random_stabilizer_circuit(n)
        g = mock.AndersWrapper(range(n))
        g.act_circuit(c)
        da = g.get_full_stabilizer().to_dictionary()

        g = mock.ABPWrapper(range(n))
        g.act_circuit(c)
        db = g.to_stabilizer().to_dictionary()

        assert da == db

