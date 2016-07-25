import numpy as np
from tqdm import tqdm
import itertools as it
from abp import clifford
from abp import build_tables
from abp import qi
from nose.tools import raises
from anders_briegel import graphsim


def identify_pauli(m):
    """ Given a signed Pauli matrix, name it. """
    for sign in (+1, -1):
        for pauli_label, pauli in zip("xyz", qi.paulis):
            if np.allclose(sign * pauli, m):
                return sign, pauli_label


def test_find_clifford():
    """ Test that slightly suspicious function """
    assert build_tables.find_clifford(qi.id, clifford.unitaries) == 0
    assert build_tables.find_clifford(qi.px, clifford.unitaries) == 1


@raises(IndexError)
def test_find_non_clifford():
    """ Test that looking for a non-Clifford gate fails """
    build_tables.find_clifford(qi.t, clifford.unitaries)


def get_action(u):
    """ What does this unitary operator do to the Paulis? """
    return [identify_pauli(u.dot(p.dot(qi.hermitian_conjugate(u)))) for p in qi.paulis]


def format_action(action):
    return "".join("{}{}".format("+" if s >= 0 else "-", p) for s, p in action)


def test_we_have_24_matrices():
    """ Check that we have 24 unique actions on the Bloch sphere """
    actions = set(tuple(get_action(u)) for u in clifford.unitaries)
    assert len(set(actions)) == 24


def test_we_have_all_useful_gates():
    """ Check that all the interesting gates are included up to a global phase """
    for name, u in qi.by_name.items():
        build_tables.find_clifford(u, clifford.unitaries)


def test_group():
    """ Test we are really in a group """
    matches = set()
    for a, b in tqdm(it.combinations(clifford.unitaries, 2), "Testing this is a group"):
        i = build_tables.find_clifford(a.dot(b), clifford.unitaries)
        matches.add(i)
    assert len(matches) == 24


def test_conjugation_table():
    """ Check that the table of Hermitian conjugates is okay """
    assert len(set(clifford.conjugation_table)) == 24


def test_cz_table_makes_sense():
    """ Test the CZ table is symmetric """
    hadamard = clifford.by_name["hadamard"]
    assert all(clifford.cz_table[0, 0, 0] == [1, 0, 0])
    assert all(clifford.cz_table[1, 0, 0] == [0, 0, 0])
    assert all(
        clifford.cz_table[0, hadamard, hadamard] == [0, hadamard, hadamard])


def test_commuters():
    """ Test that commutation is good """
    assert len(build_tables.get_commuters(clifford.unitaries)) == 4


def test_conjugation():
    """ Test that clifford.conugate() agrees with graphsim.LocCliffOp.conjugate """
    for operation_index, transform_index in it.product(range(4), range(24)):
        transform = graphsim.LocCliffOp(transform_index)
        operation = graphsim.LocCliffOp(operation_index)

        phase = operation.conjugate(transform).ph
        phase = [1, 0, -1][phase]
        new_operation = operation.op

        NEW_OPERATION, PHASE = clifford.conjugate(
            operation_index, transform_index)
        assert new_operation == NEW_OPERATION
        assert PHASE == phase


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

