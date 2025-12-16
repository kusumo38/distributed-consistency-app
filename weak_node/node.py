from flask import Flask, request, jsonify
from config import NODE_NAME, PORT

app = Flask(__name__)
data_store = {}

@app.route("/write", methods=["POST"])
def write_data():
    key = request.json["key"]
    value = request.json["value"]

    # WEAK: hanya simpan lokal
    data_store[key] = value

    return jsonify({
        "node": NODE_NAME,
        "key": key,
        "value": value,
        "note": "stored locally only (weak consistency)"
    })

@app.route("/read/<key>")
def read_data(key):
    return jsonify({
        "node": NODE_NAME,
        "value": data_store.get(key)
    })

if __name__ == "__main__":
    import os
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)

