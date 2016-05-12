from flask import Flask, request, render_template, jsonify
from werkzeug.contrib.cache import SimpleCache
import json
import abp

#TODO: only send deltas

#graphstate = abp.GraphState()
cache = SimpleCache(default_timeout = 10000)
cache.set("state", abp.GraphState())
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/state", methods = ["GET", "POST"])
def state():
    if request.method == "GET":
        state = cache.get("state")
        output = state.to_json()
        output["update_required"] = cache.get("update")
        cache.set("update", False)
        return jsonify(output)
    elif request.method == "POST":
        cache.set("update", True)
        graphstate = abp.GraphState()
        graphstate.from_json(json.loads(request.data))
        cache.set("state", graphstate)
        return jsonify({"update": "ok"})

@app.route("/add_node/<int:node>")
def add_node(node):
    """ Add a node to the graph """
    graphstate = cache.get("state")
    graphstate.add_node(node)
    graphstate.layout()
    cache.set("update", True)
    cache.set("state", graphstate)
    return jsonify({"add_node": "okay"})

@app.route("/act_local_rotation/<int:node>/<int:operation>")
def act_local_rotation(node, operation):
    """ Add a node to the graph """
    # TODO: try to lookup the operation first
    graphstate = cache.get("state")
    graphstate.act_local_rotation(node, operation)
    cache.set("update", True)
    cache.set("state", graphstate)
    return jsonify({"act_local_rotation": "okay"})

@app.route("/act_cz/<int:a>/<int:b>")
def act_cz(a, b):
    """ Add a node to the graph """
    graphstate = cache.get("state")
    graphstate.act_cz(a, b)
    graphstate.layout()
    cache.set("update", True)
    cache.set("state", graphstate)
    return jsonify({"act_cz": "okay"})

@app.route("/clear")
def clear():
    """ Clear the current state """
    graphstate = abp.GraphState()
    cache.set("update", True)
    cache.set("state", graphstate)
    return jsonify({"clear": "okay"})
    

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")


