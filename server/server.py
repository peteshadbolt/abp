from flask import Flask, request, render_template, jsonify, g
from werkzeug.contrib.cache import SimpleCache
import json
import abp
import argparse

#TODO: only send deltas

#graphstate = abp.GraphState()
cache = SimpleCache(default_timeout = 10000)
cache.set("state", abp.GraphState())
app = Flask(__name__)

@app.before_request
def before_request():
    g.state = cache.get("state")

@app.after_request
def after_request(response):
    cache.set("state", g.state)
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/state", methods = ["GET", "POST"])
def state():
    if request.method == "GET":
        output = g.state.to_json()
        output["needs_update"] = cache.get("needs_update")
        cache.set("needs_update", False)
        return jsonify(output)
    elif request.method == "POST":
        g.state = abp.GraphState()
        g.state.from_json(json.loads(request.data))
        cache.set("needs_update", True)
        return jsonify({"update": "ok"})

@app.route("/add_node/<int:node>")
def add_node(node):
    """ Add a node to the graph """
    g.state.add_node(node)
    g.state.layout()
    cache.set("needs_update", True)
    return jsonify({"add_node": "okay"})

@app.route("/act_local_rotation/<int:node>/<int:operation>")
def act_local_rotation(node, operation):
    """ Add a node to the graph """
    # TODO: try to lookup the operation first
    g.state.act_local_rotation(node, operation)
    cache.set("needs_update", True)
    return jsonify({"act_local_rotation": "okay"})

@app.route("/act_cz/<int:a>/<int:b>")
def act_cz(a, b):
    """ Add a node to the graph """
    g.state.act_cz(a, b)
    g.state.layout()
    cache.set("needs_update", True)
    return jsonify({"act_cz": "okay"})

@app.route("/clear")
def clear():
    """ Clear the current state """
    g.state = abp.GraphState()
    cache.set("needs_update", True)
    return jsonify({"clear": "okay"})
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Run in debug mode", action="store_true", default=False)
    args = parser.parse_args()
    app.debug = args.debug

    app.run(host="0.0.0.0")


