import json
import numpy as np
from abp import clifford, qi
import sys
import os
import itertools as it
from string import maketrans


def get_ab_cz_table():
    """ Load anders and briegel's CZ table """
    filename = "anders_briegel/cphase.tbl"
    filename = os.path.join(os.path.dirname(sys.path[0]), filename)
    with open(filename) as f:
        s = f.read().translate(maketrans("{}", "[]"))
        return np.array(json.loads(s))



def test_cz_table():
    """ Does our clifford code work with anders & briegel's table? """
    state_table = clifford.get_state_table(clifford.unitaries)
    ab_cz_table = get_ab_cz_table()

    rows = it.product([0, 1], it.combinations_with_replacement(range(24), 2))
    for bond, (c1, c2) in rows:

        # Pick the input state
        input_state = state_table[bond, c1, c2]

        # Go and compute the output
        computed_output = np.dot(qi.cz, input_state)
        computed_output = qi.normalize_global_phase(computed_output)

        # Now look up the answer in the table
        bondp, c1p, c2p = ab_cz_table[bond, c1, c2]
        table_output = state_table[bondp, c1p, c2p]

        assert np.allclose(computed_output, table_output)


