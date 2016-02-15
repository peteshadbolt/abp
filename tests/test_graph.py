from nose import with_setup
import abp

def setup():
    global g
    g = abp.GraphRegister(10)

@with_setup(setup)
def test_adding():
    g.add_edge(0,1)
    g.add_edge(1,2)
    g.toggle_edge(2,0)
    g.toggle_edge(2,3)
    g.toggle_edge(3,2)
    assert(len(g.edgelist()) == 3)

def setup_stab():
    global g
    g = abp.GraphRegister(10)
    g.add_edge(0,1)
    g.add_edge(1,2)
    g.add_edge(2,0)

@with_setup(setup_stab)
def test_adding():
    s = abp.Stabilizer(g)
    print s

