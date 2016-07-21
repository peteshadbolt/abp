from abp import qi

def test_dumbness():
    a = qi.CircuitModel(1)
    b = qi.CircuitModel(1)
    assert a == b

    a.act_local_rotation(0, qi.px)

    assert not (a == b)

    a.act_local_rotation(0, qi.px)

    assert (a == b)
