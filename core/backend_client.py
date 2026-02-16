import requests

BACKEND_URL = "http://127.0.0.1:8000/incident"

def send_to_backend(data):
    try:
        response = requests.post(BACKEND_URL, json=data, timeout=5)
        print("Backend response:", response.json())
    except Exception as e:
        print("Failed to send to backend:", str(e))
