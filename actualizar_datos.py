import requests
import pandas as pd
from datetime import datetime

# Configuración
PROJECT_ID = "marr-5c38a"
API_KEY = "AIzaSyBNx4SVs0PBYzTH6VKeC2Rt2or-jPNXShE"

def fetch_collection(collection_name):
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default )/documents/{collection_name}?key={API_KEY}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error en {collection_name}: {response.status_code}")
        return []
    
    data = response.json()
    documents = data.get('documents', [])
    
    rows = []
    for doc in documents:
        fields = doc.get('fields', {})
        # Extraemos los valores reales (manejando textos, números y fechas)
        row = {'ID_Registro': doc.get('name').split('/')[-1]}
        row['Tipo_Dato'] = collection_name
        
        for key, val_dict in fields.items():
            # Tomamos el primer valor que encontremos en el diccionario de Firebase
            actual_value = list(val_dict.values())[0]
            row[key] = actual_value
            
        rows.append(row)
    return rows

# 1. Intentamos bajar datos de ambas colecciones
datos_prod = fetch_collection("production")
datos_prep = fetch_collection("preparation")

todo_junto = datos_prod + datos_prep

# 2. Creamos el archivo final
if todo_junto:
    df = pd.DataFrame(todo_junto)
    # Ordenar por fecha si existe la columna timestamp
    if 'timestamp' in df.columns:
        df = df.sort_values(by='timestamp', ascending=False)
    
    df.to_csv("datos_operadores.csv", index=False)
    print(f"¡Éxito! Se guardaron {len(todo_junto)} registros.")
else:
    # Si no hay nada, creamos un archivo con un mensaje para saber qué pasó
    with open("datos_operadores.csv", "w") as f:
        f.write("Estado,Mensaje\nError,No se encontraron datos en Firebase")
    print("No se encontraron datos en las colecciones.")
