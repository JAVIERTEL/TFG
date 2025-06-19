# ==========================================================
#  Proyecto: IMPLEMENTACIÓN DE UN SISTEMA DE EVALUACIÓN DE CAPACIDADES DE GRANDES MODELOS DE LENGUAJE A TRAVÉS DE BUCLES DE RESUMEN Y EXTENSIÓN DE TEXTOS
#  Apartado: 3. DESARROLLO DEL SISTEMA EXPERIMENTAL
#            3.1 DESARROLLO DEL SISTEMA DE EVALUACIÓN BASADO EN BUCLES DE RESUMEN Y EXPANSIÓN
#  Autor: Javier González Pérez
#  Fecha: 02/12/2024
#  Descripción: Este script utiliza la API de Google AI Studios (Gemini) para realizar bucles de resumen y expansión de textos,
#               aplicando varias iteraciones sobre textos leídos desde un archivo Excel y guardando los resultados en otro archivo Excel.
# ==========================================================

import os
import time
import pandas as pd
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# Configuración de la clave API de Google AI Studios
genai.configure(api_key="tu_clave_api_google")  # Reemplaza con tu clave API de Google AI
model_name = "gemini-1.5-flash"
model = genai.GenerativeModel(model_name)

# Límites de frecuencia
REQUESTS_PER_MINUTE = 15
TOKENS_PER_MINUTE = 1_000_000
REQUESTS_PER_DAY = 1_500

# Función para resumir texto
def summary_text(model, original_text, max_summary_length, temperature=1.0):
    print(f"Resumiendo texto con el modelo {model_name} a una longitud de {max_summary_length} palabras...")
    response = model.generate_content(f"Summarize the following text to approximately {max_summary_length} words:\n\n{original_text}")
    print("Resumen generado.")
    return response.text

# Función para completar texto
def complete_text(model, summary, original_text_length, temperature=1.0):
    print(f"Expandiendo resumen a un texto de {original_text_length} palabras con el modelo {model_name}...")
    response = model.generate_content(f"Expand the following summary into a complete text of {original_text_length} words:\n\n{summary}")
    print("Texto expandido generado.")
    return response.text

# Función para iterar con seguimiento de progreso
def run_iterations(model, texts, iterations, temperature=1.0, total_steps=1, current_step=0):
    results = []
    requests_made = 0
    start_time = time.time()

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
                    summary = summary_text(model, current_text, summary_length, temperature)
                    new_text = complete_text(model, summary, original_text_length, temperature)
                    break  # Salir del bucle si la llamada fue exitosa
                except ResourceExhausted as e:
                    print(f"Error de cuota alcanzada: {e}")
                    print("Esperando 60 segundos antes de reintentar...")
                    time.sleep(60)
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

            # Control de tasa
            requests_made += 1
            if requests_made >= REQUESTS_PER_MINUTE:
                elapsed_time = time.time() - start_time
                if elapsed_time < 60:
                    time_to_wait = 60 - elapsed_time
                    print(f"Esperando {time_to_wait:.2f} segundos para respetar el límite de solicitudes por minuto...")
                    time.sleep(time_to_wait)
                requests_made = 0
                start_time = time.time()

        results.append(row)
    print(f"Modelo {model_name} completado.")
    return pd.DataFrame(results), current_step

# Leer textos desde el archivo Excel
def read_texts_from_excel(filename, start_row, limit=35): # Leer 35 textos por defecto (lo que deja como máximo)
    df = pd.read_excel(filename, skiprows=range(1, start_row))
    texts = []
    for _, row in df.iterrows():
        if len(texts) >= limit:
            break
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
    # Leer textos desde el archivo Excel (adaptar a al número de textos que faltaban por hacer )
    start_row = 290 # Empezar desde la fila 97
    texts = read_texts_from_excel('textos_gemini.xlsx', start_row=start_row, limit=10) # Número de textos a procesar
    print(f"Se han cargado {len(texts)} textos desde el archivo Excel.")

    # Configuración del modelo y parámetros
    iterations = 10
    temperature = 1.0

    # Cálculo del número total de pasos
    if texts:
        total_steps = len(texts) * iterations
        current_step = 0

        # Guardar resultados en Excel
        try:
            with pd.ExcelWriter('resultados_bucle_resumen_expansion_gemini.xlsx', mode='a', if_sheet_exists='overlay') as writer:
                print(f"Iniciando procesamiento para el modelo {model_name}...")
                sheet_name = model_name[:31]  # Limitar a 31 caracteres
                results_df, current_step = run_iterations(model, texts, iterations, temperature, total_steps, current_step)
                # Obtener la última fila ocupada en el archivo Excel
                existing_df = pd.read_excel('resultados_bucle_resumen_expansion_gemini.xlsx', sheet_name=sheet_name)
                startrow = len(existing_df) + 1
                results_df.to_excel(writer, sheet_name=sheet_name, startrow=startrow, index=False)
                print(f"Resultados guardados para el modelo {model_name}.")
        except Exception as e:
            print(f"Error al guardar el archivo Excel: {e}")
    else:
        print("No se obtuvo texto para procesar.")

    print("Proceso completado.")