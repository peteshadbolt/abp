import time, atexit, json
import networkx
import numpy as np
import websocket
from socket import error as socket_error
import graphstate
import clifford
import util

class GraphState(graphstate.GraphState, networkx.Graph):
    def __init__(self, *args, **kwargs):
        graphstate.GraphState.__init__(self, *args, **kwargs)
        self.connect_to_server()

    def connect_to_server(self, uri = "ws://localhost:5000"):
        """ Attempt to connect to the websocket server """
        try:
            self.ws = websocket.create_connection(uri)
            atexit.register(self.shutdown)
        except socket_error:
            self.ws = None

    def shutdown(self):
        """ Close the connection to the websocket """
        self.update()
        self.ws.close()

    def update(self, delay = 0.5):
        """ Call this function when you are ready to send data to the browser """
        if not self.ws:
            return

        # Automatically perform layout if position is not provided
        if not all(("position" in node) for node in self.node.values()):
            self.layout()

        #if not all(("vop" in node) for node in self.node.values()):
            #self.add_vops()

        # Send data to browser and rate-limit
        self.ws.send(json.dumps(self.to_json(), default = str))
        time.sleep(delay)

    def layout(self, dim=3):
        """ Automatically lay out the graph """
        pos = networkx.spring_layout(self, dim, scale=np.sqrt(self.order()))
        middle = np.average(pos.values(), axis=0)
        pos = {key: value - middle for key, value in pos.items()}
        for key, (x, y, z) in pos.items():
            self.node[key]["position"] = util.xyz(x, y, z)

    def add_vops(self):
        """ Automatically add vops if they're not present """
        for key in self.node:
            if not "vop" in self.node[key]:
                self.node[key]["vop"] = clifford.by_name["identity"]

        
