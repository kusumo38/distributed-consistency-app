from flask import Flask, request, jsonify
import requests
import threading
import time
from config import NODE_NAME, PORT, OTHER_NODES

app = Flask(__name__)
store = {}

@app.route("/write", methods=["POST"])
def write():
    data = request.json
    key = data["key"]
    value = data["value"]

    # simpan lokal dulu
    store[key] = value
    print(f"[EVENTUAL] WRITE LOCAL:", key, value)

    def delayed_sync():
        time.sleep(5)  # ⏱ delay 5 detik
        for peer in OTHER_NODES:
            try:
                print(f"[EVENTUAL] REPLICATE TO {peer}")
                requests.post(f"{peer}/replicate", json=data)
            except Exception as e:
                print("Replication failed:", e)

    # sync async (eventual)
    threading.Thread(target=delayed_sync).start()

    return jsonify({
        "node": NODE_NAME,
        "status": "eventual write accepted",
        "key": key,
        "value": value
    })

@app.route("/replicate", methods=["POST"])
def replicate():
    data = request.json
    store[data["key"]] = data["value"]
    print(f"[EVENTUAL] REPLICATED:", data)
    return jsonify({"status": "replicated"})

@app.route("/read/<key>")
def read(key):
    return jsonify({
        "node": NODE_NAME,
        "value": store.get(key)
    })

if __name__ == "__main__":
    import os
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
