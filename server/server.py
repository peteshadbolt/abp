import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import sys, json, time, os
from graphstate import GraphState
import requests


class VizHandler(SimpleHTTPRequestHandler):

    """ Handles requests to the server """

    def get_state(self):
        """ Get the current graphstate state """
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(state.to_json())

    def do_GET(self, *args, **kwargs):
        """ Someone belled the server """
        parsed_path = urlparse.urlparse(self.path)
        if parsed_path.path == "/state":
            return self.get_state()
        else:
            return SimpleHTTPRequestHandler.do_GET(self, *args, **kwargs)


class Server(SocketServer.TCPServer):

    """ Serves the good stuff """
    allow_reuse_address = True

    def __init__(self, port=8000):
        self.port = port
        self.state = None
        SocketServer.TCPServer.__init__(self, ("127.0.0.1", self.port), VizHandler)
        print "Serving on port {} (Press CTRL-C to quit)".format(self.port)
        self.serve_forever()


if __name__ == '__main__':
    os.chdir(os.path.join(sys.path[0], "../static"))
    server = Server()
    server.shutdown()

    requests.get("http://localhost:8000/state")
