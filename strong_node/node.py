from flask import Flask, request, jsonify
import requests
import threading
import time
from config import NODE_NAME, PORT, OTHER_NODES

app = Flask(__name__)
data_store = {}

@app.route("/write", methods=["POST"])
def write_data():
    key = request.json["key"]
    value = request.json["value"]

    data_store[key] = value

    if NODE_NAME == "STRONG":
        for node in OTHER_NODES:
            requests.post(f"{node}/replicate",
                          json={"key": key, "value": value})

    elif NODE_NAME == "EVENTUAL":
        threading.Thread(
            target=eventual_sync,
            args=(key, value)
        ).start()

    return jsonify({
        "node": NODE_NAME,
        "key": key,
        "value": value
    })

@app.route("/replicate", methods=["POST"])
def replicate():
    key = request.json["key"]
    value = request.json["value"]
    data_store[key] = value
    return jsonify({"status": "replicated"})

@app.route("/read/<key>")
def read_data(key):
    return jsonify({
        "node": NODE_NAME,
        "value": data_store.get(key)
    })

def eventual_sync(key, value):
    time.sleep(5)
    for node in OTHER_NODES:
        requests.post(f"{node}/replicate",
                      json={"key": key, "value": value})

if __name__ == "__main__":
    import os
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)

