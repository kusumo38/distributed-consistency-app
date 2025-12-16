import requests
import time

NODE_URL = "http://localhost:5001"  # EVENTUAL

payload = {
    "key": "saldo",
    "value": 900000
}

print("\n=== WRITE KE EVENTUAL ===")
requests.post(f"{NODE_URL}/write", json=payload)

print("\n=== READ LANGSUNG ===")
for url in [
    "http://localhost:5000",
    "http://localhost:5001",
    "http://localhost:5002"
]:
    print(url, requests.get(f"{url}/read/saldo").json())

print("\n⏳ TUNGGU 6 DETIK...\n")
time.sleep(6)

print("=== READ SETELAH DELAY ===")
for url in [
    "http://localhost:5000",
    "http://localhost:5001",
    "http://localhost:5002"
]:
    print(url, requests.get(f"{url}/read/saldo").json())
