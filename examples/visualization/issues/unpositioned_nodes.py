from abp.fancy import GraphState
import networkx as nx

edges = [(0,1),(1,2),(2,3),(3,4)]
nodes = [(i, {'x': i, 'y': 0, 'z':0}) for i in range(5)]
gs = GraphState()

for node, position in nodes:
    gs.add_qubit(node, position=position)
    gs.act_hadamard(node)

for edge in edges:
    gs.act_cz(*edge)
gs.update(3)
# a single line of qubits are created along the x axis
gs.add_qubit('start')
gs.update(0)
# a curved 5-qubit cluster and single qubit is depicted
