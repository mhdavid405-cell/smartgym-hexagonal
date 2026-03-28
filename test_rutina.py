import requests
import json

url = "http://localhost:5000/api/rutinas"
data = {
    "cliente_id": 1,
    "titulo": "Rutina de prueba",
    "ejercicios": "Press banca 3x12, Sentadillas 4x10"
}

print(f"Enviando: {json.dumps(data)}")
response = requests.post(url, json=data)

print(f"\nStatus Code: {response.status_code}")
print(f"Response: {response.json()}")
