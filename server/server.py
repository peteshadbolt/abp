from flask import Flask, request, render_template, jsonify
import json
import abp

graphstate = abp.GraphState()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/state", methods = ["GET", "POST"])
def state():
    if request.method == "GET":
        return jsonify(graphstate.to_json())
    elif request.method == "POST":
        graphstate.from_json(json.loads(request.data))
        return jsonify(graphstate.to_json())

@app.route("/add/<int:node>")
def add(node):
    """ Add a node to the graph """
    graphstate.add_node(node)
    return jsonify(graphstate.to_json())

@app.route("/rotate/<int:node>/<int:operation>")
def rotate(node):
    """ Add a node to the graph """
    graphstate.act_local_rotation(node, operation)
    return jsonify(graphstate.to_json())

@app.route("/cz/<int:a>/<int:b>")
def cz(a, b):
    """ Add a node to the graph """
    graphstate.act_cz(a, b)
    return jsonify(graphstate.to_json())

@app.route("/clear")
def clear():
    """ Clear the current state """
    graphstate = abp.GraphState()
    return jsonify({"clear": "ok"})
    

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")


