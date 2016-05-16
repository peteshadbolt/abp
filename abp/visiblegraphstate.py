"""
Allows us to visualize the state in a browser
"""

import atexit
import threading
import time
from websocket import create_connection
from graphstate import GraphState
import json

class VisibleGraphState(GraphState):

    def __init__(self, *args, **kwargs):
        GraphState.__init__(self, *args, **kwargs)
        self.ws = create_connection("ws://localhost:5001")
        self.diff = []
        atexit.register(self.shutdown)
        self.ws.send(json.dumps({"method":"clear"}))

    def shutdown(self):
        if len(self.diff)>0:
            self.update()
        self.ws.close()

    def send(self, method, *args, **kwargs):
        kwargs.update({"method": method})
        self.diff.append(kwargs)

    def add_node(self, node, meta = {}):
        GraphState.add_node(self, node, meta)
        self.send("add_node", node=node, meta=meta)

    def add_edge(self, start, end):
        GraphState.add_edge(self, start, end)
        self.send("add_edge", start=start, end=end)

    def del_edge(self, start, end):
        GraphState.del_edge(self, start, end)
        self.send("del_edge", start=start, end=end)

    def act_local_rotation(self, node, operation):
        GraphState.act_local_rotation(self, node, operation)
        self.send("update_vop", node = node, vop = self.vops[node])

    def update(self):
        #data = json.dumps({"diff": self.diff, "state":self.to_json()})
        data = json.dumps({"diff": self.diff})
        self.ws.send(data)
        self.diff = []

