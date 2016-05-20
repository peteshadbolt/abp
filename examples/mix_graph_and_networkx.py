from abp.fancy import GraphState

g = GraphState()
n = 100
g.add_nodes_from(range(n))
g.add_edges_from([i, i+1] for i in range(n-1))
