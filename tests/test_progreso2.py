import requests
import json

url = "http://localhost:5000/api/progreso"
data = {
    "cliente_id": 1,
    "peso": 74.0,
    "brazos": 35.5,
    "pecho": 96,
    "notas": "Segunda medición - progreso"
}

response = requests.post(url, json=data)
print(f"Status: {response.status_code}")
print(response.json())
