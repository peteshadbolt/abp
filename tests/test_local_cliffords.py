import local_cliffords as lc

def test_identify_pauli():
    assert lc.identify_pauli(lc.px) == "+x"
    assert lc.identify_pauli(-lc.px) == "-x"
    assert lc.identify_pauli(-lc.pz) == "-z"

def test_get_action():
    assert lc.get_action(lc.i) == ("+x", "+y", "+z")
