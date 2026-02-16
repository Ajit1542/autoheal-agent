import requests
from core.logger import log

BACKEND_URL = "http://127.0.0.1:8000/incident"

def send_to_backend(data):
    log(f"Sending {len(data)} incidents to backend")
    try:
        response = requests.post(BACKEND_URL, json=data, timeout=5)
        log(f"Backend response: {response.status_code} | {response.text}")
    except Exception as e:
        log(f"Failed to send to backend: {e}", level="ERROR")
