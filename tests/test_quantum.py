from abp.graphstate import GraphState

def test_logic_101():
    """ Some really simple tests """
    g = GraphState()
    g.act_local_rotation_by_name(0, "hadamard")
    #print g.

