import time, atexit, json
import sys
import networkx as nx
import numpy as np
import websocket
from socket import error as socket_error
import graphstate
import clifford
import util

class GraphState(graphstate.GraphState, nx.Graph):
    def __init__(self, *args, **kwargs):
        if type(args[0])==nx.Graph:
            self.from_nx(args[0])
        else:
            graphstate.GraphState.__init__(self, *args, **kwargs)
        self.connect_to_server()

    def connect_to_server(self, uri = "ws://localhost:5000"):
        """ Attempt to connect to the websocket server """
        try:
            self.ws = websocket.create_connection(uri, timeout=0.1)
            atexit.register(self.shutdown)
        except: #TODO: bad practice
            self.ws = None

    def from_nx(self, g):
        """ Clone from a networkx graph. Hacky af """
        self.adj = g.adj.copy()
        self.node = g.node.copy()
        # TODO: hacky af
        for key, value in self.node.items():
            self.node[key]["vop"] = clifford.by_name["identity"]


    def shutdown(self):
        """ Close the connection to the websocket """
        if not self.ws:
            return
        self.update()
        self.ws.close()

    def update(self, delay = 0.5):
        """ Call this function when you are ready to send data to the browser """
        if not self.ws:
            return

        # Automatically perform layout if position is not provided
        if not all(("position" in node) for node in self.node.values()):
            self.layout()

        # Send data to browser and rate-limit
        try:
            self.ws.send(json.dumps(self.to_json(stringify=True)))
            self.ws.recv()
            time.sleep(delay)
        except websocket._exceptions.WebSocketTimeoutException:
            print "Timed out ... you might be pushing a bit hard"
            sys.exit(0)
            #self.ws.close()
            #self.connect_to_server()

    def layout(self):
        """ Automatically lay out the graph """
        pos = nx.spring_layout(self, dim=3, scale=np.sqrt(self.order()))
        middle = np.average(pos.values(), axis=0)
        pos = {key: value - middle for key, value in pos.items()}
        for key, (x, y, z) in pos.items():
            self.node[key]["position"] = util.xyz(x, y, z)

    def add_vops(self):
        """ Automatically add vops if they're not present """
        for key in self.node:
            if not "vop" in self.node[key]:
                self.node[key]["vop"] = clifford.by_name["identity"]

        
