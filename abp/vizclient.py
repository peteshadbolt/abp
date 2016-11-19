import time, atexit, json
import networkx as nx
import numpy as np
import websocket
from socket import error as socket_error
import clifford
import util
import nxgraphstate

class VizClient(object):
    def __init__(self, uri = "ws://localhost:5000"):
        self.ws = websocket.create_connection(uri, timeout=0.1)
        atexit.register(self.shutdown)

    def shutdown(self):
        """ Close the connection to the websocket """
        self.ws.close()

    def update(self, graph, delay = 0.5):
        """ Call this function when you are ready to send data to the browser """
        g = nxgraphstate.NXGraphState(graph)

        # Automatically perform layout if position is not provided
        if not all(("position" in node) for node in g.node.values()):
            g.layout()

        # Send data to browser and rate-limit
        try:
            self.ws.send(json.dumps(g.to_json(stringify=True)))
            self.ws.recv()
        except websocket._exceptions.WebSocketTimeoutException:
            print "Timed out ... you might be pushing a bit hard"
        time.sleep(delay)


