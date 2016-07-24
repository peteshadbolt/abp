import numpy as np
from abp import clifford, qi, build_tables
import itertools as it

def test_cz_table():
    """ Does the CZ code work good? """
    state_table = build_tables.get_state_table(clifford.unitaries)

    rows = it.product([0, 1], it.combinations_with_replacement(range(24), 2))

    for bond, (c1, c2) in rows:

        # Pick the input state
        input_state = state_table[bond, c1, c2]

        # Go and compute the output
        computed_output = np.dot(qi.cz, input_state)
        computed_output = qi.normalize_global_phase(computed_output)

        # Now look up the answer in the table
        bondp, c1p, c2p = clifford.cz_table[bond, c1, c2]
        table_output = state_table[bondp, c1p, c2p]

        assert np.allclose(computed_output, table_output)



