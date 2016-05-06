import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import sys
import json
import threading
import time

class MyHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        SimpleHTTPRequestHandler.__init__(self, *args, **kwargs)

    def get_state(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"state":"here is the state"}))
    
    def do_GET(self, *args, **kwargs):
        parsed_path = urlparse.urlparse(self.path)
        print parsed_path.path
        if parsed_path.path == "/state":
            return self.get_state()
        else:
            return SimpleHTTPRequestHandler.do_GET(self, *args, **kwargs)

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv)==2 else 8000
    server = SocketServer.TCPServer(("127.0.0.1", port), MyHandler)

    print "Go to 127.0.0.0:{}".format(port)
    thread = threading.Thread(None, server.serve_forever)
    thread.daemon = True
    thread.start()
    time.sleep(5)
    print "Shutting down ... "
    server.shutdown()
    #thread.join()
