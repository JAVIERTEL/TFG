# ==========================================================
#  Proyecto: IMPLEMENTACIÓN DE UN SISTEMA DE EVALUACIÓN DE CAPACIDADES DE GRANDES MODELOS DE LENGUAJE A TRAVÉS DE BUCLES DE RESUMEN Y EXTENSIÓN DE TEXTOS
#  Apartado: 3. DESARROLLO DEL SISTEMA EXPERIMENTAL
#            3.1 DESARROLLO DEL SISTEMA DE EVALUACIÓN BASADO EN BUCLES DE RESUMEN Y EXPANSIÓN
#  Autor: Javier González Pérez
#  Fecha: 02/12/2024
#  Descripción: Este script utiliza la API de Groq para realizar bucles de resumen y expansión de textos,
#               aplicando varias iteraciones sobre textos leídos desde un archivo Excel y guardando los resultados en otro archivo Excel.
# ==========================================================

import os
import pandas as pd
from openai import OpenAI

# Configuración del cliente de OpenAI
client = OpenAI(api_key="tu_clave_api_openai")  # Reemplaza con tu clave API de OpenAI

# Función para crear el archivo Excel si no existe
def ensure_excel_file_exists(filename):
    if not os.path.exists(filename):
        print(f"El archivo {filename} no existe. Creándolo...")
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Crear un archivo vacío con una hoja inicial
            pd.DataFrame().to_excel(writer, sheet_name="Hoja1", index=False)
        print(f"Archivo {filename} creado exitosamente.")

# Función para resumir texto
def summary_text(client, model, original_text, max_summary_length, temperature=1.0):
    print(f"Resumiendo texto con el modelo {model} a una longitud de {max_summary_length} palabras...")
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"Summarize the following text to approximately {max_summary_length} words:"},
            {"role": "user", "content": original_text},
        ],
        temperature=temperature,
    )
    print("Resumen generado.")
    return completion.choices[0].message.content

# Función para completar texto
def complete_text(client, model, summary, original_text_length, temperature=1.0):
    print(f"Expandiendo resumen a un texto de {original_text_length} palabras con el modelo {model}...")
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"Expand the following summary into a complete text of {original_text_length} words:"},
            {"role": "user", "content": summary},
        ],
        temperature=temperature,
    )
    print("Texto expandido generado.")
    return completion.choices[0].message.content

# Función para iterar con seguimiento de progreso
def run_iterations(client, model, texts, iterations, temperature=1.0, total_steps=1, current_step=0):
    results = []
    for text_idx, text_data in enumerate(texts):
        print(f"Procesando texto {text_idx + 1}/{len(texts)}...")
        row = {
            'id': text_data['id'],
            'original_text': text_data['original_text'],
            'original_text_length': text_data['original_text_length'],
            'original_summary': text_data['original_summary'],
            'original_summary_length': text_data['original_summary_length']
        }
        
        # Inicializar el texto actual con el texto original
        current_text = text_data['original_text']

        for i in range(iterations):
            print(f"Iteración {i + 1}/{iterations} con temperatura {temperature}...")
            original_text_length = text_data['original_text_length']
            summary_length = text_data['original_summary_length']

            # Implementar reintentos para las llamadas a la API
            for attempt in range(3):  # Intentar hasta 3 veces
                try:
                    summary = summary_text(client, model, current_text, summary_length, temperature)
                    new_text = complete_text(client, model, summary, original_text_length, temperature)
                    break  # Salir del bucle si la llamada fue exitosa
                except Exception as e:
                    print(f"Error en la llamada a la API: {e}")
                    if attempt == 2:  # Si es el último intento, asignar valores predeterminados
                        summary = "Resumen no disponible"
                        new_text = "Texto no disponible"
                    else:
                        print("Reintentando...")

            row[f'summary_{i + 1}_temp_{temperature}'] = summary
            row[f'new_text_{i + 1}_temp_{temperature}'] = new_text

            # Actualizar el texto actual para la siguiente iteración
            current_text = new_text

            # Actualizar el progreso
            current_step += 1
            progress = (current_step / total_steps) * 100
            print(f"Progreso: {progress:.2f}% (Texto {text_idx + 1}, Iteración {i + 1}, Temperatura {temperature})")

        results.append(row)
    print(f"Modelo {model} completado.")
    return pd.DataFrame(results), current_step

# Leer textos desde el archivo Excel
def read_texts_from_excel(filename, start_row):
    df = pd.read_excel(filename, skiprows=range(1, start_row))
    texts = []
    for _, row in df.iterrows():
        text_data = {
            'id': row['id'],
            'original_text': row['original_text'],
            'original_text_length': row['original_text_length'],
            'original_summary': row['original_summary'],
            'original_summary_length': row['original_summary_length']
        }
        texts.append(text_data)
    return texts

# Main
if __name__ == "__main__":
    # Leer textos desde el archivo Excel (todos los textos a partir de la fila especificada)
    start_row = 0  # Empezar desde la primera fila
    texts = read_texts_from_excel('texts_dailymail.xlsx', start_row=start_row)
    print(f"Se han cargado {len(texts)} textos desde el archivo Excel.")

    # Configuración del modelo y parámetros
    iterations = 10
    temperature = 1.0
    model = "gpt-4o-mini-2024-07-18"

    # Nombre del archivo de salida
    output_file = 'output_gpt4-mini.xlsx'

    # Asegurarse de que el archivo Excel exista
    ensure_excel_file_exists(output_file)

    # Cálculo del número total de pasos
    if texts:
        total_steps = len(texts) * iterations
        current_step = 0

        # Guardar resultados en Excel
        with pd.ExcelWriter(output_file, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
            print(f"Iniciando procesamiento para el modelo {model}...")
            sheet_name = model[:31]  # Limitar a 31 caracteres
            results_df, current_step = run_iterations(client, model, texts, iterations, temperature, total_steps, current_step)
            # Obtener la última fila ocupada en el archivo Excel
            try:
                existing_df = pd.read_excel(output_file, sheet_name=sheet_name)
                startrow = len(existing_df) + 1
            except ValueError:
                startrow = 0
            results_df.to_excel(writer, sheet_name=sheet_name, startrow=startrow, index=False)
            print(f"Resultados guardados para el modelo {model}.")
    else:
        print("No se obtuvo texto para procesar.")

    print("Proceso completado.")