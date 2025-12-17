from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
data_store = {}

NODE_NAME = "STRONG"
OTHER_NODES = os.environ.get("OTHER_NODES", "").split(",")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "STRONG NODE RUNNING"})

@app.route("/write", methods=["POST"])
def write():
    data = request.json
    key = data["key"]
    value = data["value"]

    data_store[key] = value

    # Strong consistency: langsung replikasi
    for node in OTHER_NODES:
        if node:
            try:
                requests.post(f"{node}/replicate", json=data, timeout=3)
            except:
                pass

    return jsonify({
        "node": NODE_NAME,
        "key": key,
        "value": value
    })

@app.route("/replicate", methods=["POST"])
def replicate():
    data = request.json
    data_store[data["key"]] = data["value"]
    return jsonify({"status": "replicated"})

@app.route("/read/<key>", methods=["GET"])
def read(key):
    return jsonify({
        "node": NODE_NAME,
        "value": data_store.get(key)
    })

# ⛔ JANGAN ADA app.run()
