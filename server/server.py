from flask import Flask, request, render_template, jsonify
from flask_sockets import Sockets
from werkzeug.contrib.cache import SimpleCache
import werkzeug.serving
import json
import abp

cache = SimpleCache(default_timeout = 10000)
cache.set("state", abp.GraphState())
app = Flask(__name__)
sockets = Sockets(app)

@app.route("/")
def index():
    return render_template("index.html")

@sockets.route('/diff')
def diff_socket(ws):
    while not ws.closed:
        message = ws.receive()
        print message
        ws.send("Hi from the server, you said '{}'".format(message))

@werkzeug.serving.run_with_reloader
def runServer():
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    app.debug = True
    ws = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    ws.serve_forever()

