import abp
import atexit
import json
from websocket import create_connection

class ServedState(abp.GraphState):
    def __init__(self):
        abp.GraphState.__init__(self) 
        self.ws = create_connection("ws://localhost:5001")
        atexit.register(self.ws.close)
        self.send("clear")

    def send(self, method, *args, **kwargs):
        kwargs.update({"method":method})
        self.ws.send(json.dumps(kwargs))

    def add_node(self, node):
        abp.GraphState.add_node(self, node)
        self.send("add_node", node = node)

    def add_edge(self, start, end):
        abp.GraphState.add_edge(self, start, end)
        self.send("add_edge", start = start, end = end)

    def del_edge(self, start, end):
        abp.GraphState.del_edge(self, start, end)
        self.send("del_edge", start = start, end = end)

    def del_edge(self, start, end):
        abp.GraphState.del_edge(self, start, end)
        self.send("del_edge", start = start, end = end)


if __name__ == '__main__':
    s = ServedState()
    s.add_node(0)
    s.add_node(1)
    s.add_edge(0,1)
