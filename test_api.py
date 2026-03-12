import requests

url = "http://localhost:8069/api/plc_data"

payload = {
    "machine": "TEST_MACHINE",
    "good": 10,
    "reject": 1,
    "status": 1,
    "cycle": 45
}

response = requests.post(url, json=payload)

print(response.text)