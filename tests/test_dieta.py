import requests
import json

url = "http://localhost:5000/api/dietas"
data = {
    "cliente_id": 1,
    "titulo": "Dieta de volumen",
    "descripcion": "Plan alimenticio para aumento de masa muscular",
    "comidas": "Desayuno: Avena con huevos, Almuerzo: Pollo con arroz, Cena: Pescado con verduras"
}

print(f"Enviando: {json.dumps(data)}")
response = requests.post(url, json=data)

print(f"\nStatus Code: {response.status_code}")
print(f"Response: {response.json()}")
