from flask import Flask, request, render_template, jsonify
import abp

graphstate = abp.GraphState()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/state")
def state():
    if request.method == "GET":
        return jsonify(graphstate.to_json())
    elif request.method == "POST":
        graphstate.from_json(request.data)
        return jsonify(graphstate.to_json())

@app.route("/state")
def state():
    return jsonify(graphstate.to_json())

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")


