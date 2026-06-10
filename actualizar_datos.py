import requests
import pandas as pd

# Datos de tu sistema
PROJECT_ID = "marr-5c38a"
API_KEY = "AIzaSyBNx4SVs0PBYzTH6VKeC2Rt2or-jPNXShE"

def fetch_data(collection):
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default )/documents/{collection}?key={API_KEY}"
    res = requests.get(url)
    if res.status_code != 200: return []
    docs = res.json().get('documents', [])
    rows = []
    for doc in docs:
        fields = doc.get('fields', {})
        # Limpiamos los datos para que Power BI los entienda
        row = {k: list(v.values())[0] for k, v in fields.items()}
        rows.append(row)
    return rows

# Bajamos los datos de produccion
data = fetch_data("production")
df = pd.DataFrame(data)
df.to_csv("datos_operadores.csv", index=False)
print("Archivo CSV creado con éxito")
