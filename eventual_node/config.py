import os

NODE_NAME = "EVENTUAL"  # ganti sesuai node
PORT = int(os.environ.get("PORT", 5001))

OTHER_NODES = [
    "https://strong-node.up.railway.app"
]
