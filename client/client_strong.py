import requests

NODE_URL = "http://localhost:5000"  # STRONG

payload = {
    "key": "saldo",
    "value": 1000000
}

print("\n=== CLIENT STRONG WRITE ===")
requests.post(f"{NODE_URL}/write", json=payload)

print("\n=== READ SEMUA NODE ===")
for url in [
    "http://localhost:5000",
    "http://localhost:5001",
    "http://localhost:5002"
]:
    print(url, requests.get(f"{url}/read/saldo").json())
