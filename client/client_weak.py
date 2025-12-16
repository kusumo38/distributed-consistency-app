import requests

NODE_URL = "http://localhost:5002"  # WEAK

payload = {
    "key": "saldo",
    "value": 800000
}

print("\n=== CLIENT WEAK WRITE ===")
requests.post(f"{NODE_URL}/write", json=payload)

print("\n=== READ SEMUA NODE ===")
for url in [
    "http://localhost:5000",
    "http://localhost:5001",
    "http://localhost:5002"
]:
    print(url, requests.get(f"{url}/read/saldo").json())
