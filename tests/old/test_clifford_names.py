from abp import clifford

def test_names():
    """ Test the naming scheme """
    for i in range(24):
        clifford.get_name(i)
    assert clifford.get_name(16)=="IE"
