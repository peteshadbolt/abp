from graph import *

def test_local_complementation():
    """ Test that local complementation works as expected """
    g, vops = graph()
    add_edge(g, 0, 1)
    add_edge(g, 0, 2)
    add_edge(g, 1, 2)
    add_edge(g, 0, 3)
    local_complementation(g, vops, 0)
    assert has_edge(g, 0, 1)
    assert has_edge(g, 0, 2)
    assert not has_edge(g, 1, 2)
    assert has_edge(g, 3, 2)
    assert has_edge(g, 3, 1)

    # TODO: test VOP conditions

def test_remove_vop():
    """ Test that removing VOPs really works """
    pass

    
