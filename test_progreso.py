import requests
import json
from datetime import datetime

url = "http://localhost:5000/api/progreso"
data = {
    "cliente_id": 1,
    "peso": 75.5,
    "altura": 175,
    "brazos": 35,
    "pecho": 95,
    "cintura": 80,
    "piernas": 60,
    "notas": "Primera medición"
}

print(f"Enviando: {json.dumps(data)}")
response = requests.post(url, json=data)

print(f"\nStatus Code: {response.status_code}")
print(f"Response: {response.json()}")
