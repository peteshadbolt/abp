from abp import clifford
from abp import qi
import numpy as np

def test_normalize_global_phase():
    for i in range(10):
        u = qi.pz
        phase = np.random.uniform(0, 2*np.pi)
        m = np.exp(1j*phase) * u
        normalized = qi.normalize_global_phase(m)
        assert np.allclose(normalized, u)
