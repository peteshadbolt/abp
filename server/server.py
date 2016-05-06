import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer

class MyHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        SimpleHTTPRequestHandler.__init__(self, *args, **kwargs)

    def get_state(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write("here is the state")
    
    def do_GET(self, *args, **kwargs):
        parsed_path = urlparse.urlparse(self.path)
        if parsed_path == "/state":
            return self.get_state()
        else:
            return SimpleHTTPRequestHandler.do_GET(self, *args, **kwargs)



httpd = SocketServer.TCPServer(("", 8000), MyHandler)

print "Go to 127.0.0.0:8000"
httpd.serve_forever()
