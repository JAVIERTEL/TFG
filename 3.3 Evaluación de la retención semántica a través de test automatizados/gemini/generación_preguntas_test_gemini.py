# ==========================================================
#  Proyecto: IMPLEMENTACIÓN DE UN SISTEMA DE EVALUACIÓN DE CAPACIDADES DE GRANDES MODELOS DE LENGUAJE A TRAVÉS DE BUCLES DE RESUMEN Y EXTENSIÓN DE TEXTOS
#  Apartado: 3. DESARROLLO DEL SISTEMA EXPERIMENTAL
#            3.3 EVALUACIÓN DE LA RETENCIÓN SEMÁNTICA A TRAVÉS DE TEST AUTOMATIZADOS
#  Autor: Javier González Pérez
#  Fecha: 25/05/2025
#  Descripción: Este script utiliza la API de Google AI Studio (Gemini) para generar preguntas tipo test a partir de textos originales
#               leídos desde un archivo Excel, formatea las preguntas y guarda los resultados
# ==========================================================

import os
import time
import json
import pandas as pd
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# Configura tu API Key de Google AI Studio
genai.configure(api_key="")  # Sustituye por tu API KEY real

model_name = "gemini-1.5-flash"
model = genai.GenerativeModel(model_name)

# Parámetros
input_file = "textos_gemini.xlsx"
output_file = "test_questions_gemini_incremental_v2.jsonl"
start_row = 0  # Cambiado a 0 para no omitir filas importantes
limit = 300
REQUESTS_PER_MINUTE = 15

# Cargar IDs ya procesados
def load_processed_ids(output_file):
    processed_ids = set()
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    processed_ids.add(data["id"])
                except Exception:
                    continue
    return processed_ids

# Leer los textos desde Excel
def read_texts(filename, start_row, limit):
    df = pd.read_excel(filename, skiprows=start_row)  # Ajustado para no omitir encabezados
    texts = []
    for _, row in df.iterrows():
        if len(texts) >= limit:
            break
        if pd.notna(row['original_text']):
            texts.append({'id': row['id'], 'original_text': row['original_text']})
    return texts

# Generar preguntas tipo test con formato consistente
def generate_questions(text):
    prompt = (
        "Generate 10 multiple-choice questions based on the following text. "
        "Each question should have four answer options (A, B, C, and D), with only one correct answer. "
        "The correct answer must always be explicitly stated after the options in the format: '**Correct Answer: X**'. "
        "Ensure all questions and options are complete and follow this structure:\n\n"
        "1. Question text?\n"
        "    A) Option 1\n"
        "    B) Option 2\n"
        "    C) Option 3\n"
        "    D) Option 4\n"
        "    **Correct Answer: X**\n\n"
        f"{text}"
    )
    response = model.generate_content(prompt)
    return response.text

# Reestructurar preguntas para garantizar formato consistente
def reformat_questions(output):
    lines = output.split("\n")
    reformatted = []
    current_question = {}
    for line in lines:
        line = line.strip()
        if line.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.")):
            if current_question:
                reformatted.append(current_question)
                current_question = {}
            current_question["question"] = line
            current_question["options"] = []
        elif line.startswith(("A)", "B)", "C)", "D)")):
            current_question["options"].append(line)
        elif "**Correct Answer:" in line:
            current_question["correct_answer"] = line.split("**Correct Answer:")[1].strip()
    if current_question:
        reformatted.append(current_question)
    return reformatted

# Guardar resultado en .jsonl (modo append)
def append_result(entry, filename):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# MAIN
if __name__ == "__main__":
    texts = read_texts(input_file, start_row, limit)
    print(f"Textos cargados: {len(texts)}")

    processed_ids = load_processed_ids(output_file)
    print(f"Textos ya procesados: {len(processed_ids)}")

    requests_made = 0
    start_time = time.time()

    for idx, item in enumerate(texts):
        text_id = item['id']
        if text_id in processed_ids:
            print(f"Saltando ID ya procesado: {text_id}")
            continue

        print(f"Procesando texto {idx + 1}/{len(texts)} - ID: {text_id}")

        try:
            output = generate_questions(item['original_text'])
            reformatted_output = reformat_questions(output)
        except ResourceExhausted:
            print("Límite de tokens alcanzado. Esperando 60 segundos...")
            time.sleep(60)
            continue
        except Exception as e:
            print(f"Error en ID {text_id}: {e}")
            reformatted_output = "ERROR"

        result = {"id": text_id, "questions_output": reformatted_output}
        append_result(result, output_file)

        # Control de tasa
        requests_made += 1
        if requests_made >= REQUESTS_PER_MINUTE:
            elapsed = time.time() - start_time
            if elapsed < 60:
                wait = 60 - elapsed
                print(f"Esperando {wait:.2f} segundos por límite de RPM...")
                time.sleep(wait)
            requests_made = 0
            start_time = time.time()

    print(f"Proceso completado. Resultados guardados en {output_file}")