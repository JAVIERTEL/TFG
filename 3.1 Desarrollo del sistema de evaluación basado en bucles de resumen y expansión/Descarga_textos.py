# ==========================================================
#  Proyecto: IMPLEMENTACIÓN DE UN SISTEMA DE EVALUACIÓN DE CAPACIDADES DE GRANDES MODELOS DE LENGUAJE A TRAVÉS DE BUCLES DE RESUMEN Y EXTENSIÓN DE TEXTOS
#  Apartado: 3. DESARROLLO DEL SISTEMA EXPERIMENTAL
#            3.1 DESARROLLO DEL SISTEMA DE EVALUACIÓN BASADO EN BUCLES DE RESUMEN Y EXPANSIÓN
#  Autor: Javier González Pérez
#  Fecha: 20/11/2024
#  Descripción: Este script descarga textos y resúmenes del dataset CNN/DailyMail usando la API de Hugging Face,
#               y guarda los resultados en un archivo Excel.
# ==========================================================
import os
import requests
import pandas as pd

# Configuración de la clave Hugging Faces
huggingface_token = ""  # Reemplaza con tu token de Hugging Face
headers = {"Authorization": f"Bearer {huggingface_token}"}

# Función para obtener un texto desde el dataset CNN/DailyMail
def fetch_single_text(offset):
    url = "https://datasets-server.huggingface.co/rows"
    params = {
        "dataset": "abisee/cnn_dailymail",  # Nombre del dataset
        "config": "3.0.0",                  # Configuración del dataset
        "split": "train",                   # Split del dataset
        "offset": offset,                   # Inicio (primer texto)
        "length": 1                         # Solo un texto
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'rows' in data and len(data['rows']) > 0:
            row = data['rows'][0]['row']
            return {
                "id": row.get('id', 'Sin ID'),
                "original_text": row.get('article', 'Texto no disponible'),
                "original_text_length": len(row.get('article', '').split()),
                "original_summary": row.get('highlights', 'Resumen no disponible'),
                "original_summary_length": len(row.get('highlights', '').split())
            }
        else:
            return None
    else:
        return None

# Guardar datos en un archivo Excel
def save_to_excel(data, filename="Nombre_fichero_de_salida.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Datos guardados correctamente en {filename}.")

# Main
if __name__ == "__main__":
    texts = []
    offset =  # Indica por el texto por el que se empieza 

    while len(texts) < 1000:
        text_data = fetch_single_text(offset)
        offset += 1

        if text_data:
            texts.append(text_data)

        # Añadir trazas para ver el progreso
        if offset % 10 == 0:
            print(f"Textos procesados: {offset}, Textos descargados: {len(texts)}")

    print(f"Total de textos descargados: {len(texts)}")

    if texts:
        save_to_excel(texts)
    else:
        print("No se pudieron descargar suficientes textos.")