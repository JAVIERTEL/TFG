# ==========================================================
#  Proyecto: 
#  Apartado: 3. DESARROLLO DEL SISTEMA EXPERIMENTAL
#            3.3 EVALUACIÓN DE LA RETENCIÓN SEMÁNTICA A TRAVÉS DE TEST AUTOMATIZADOS
#  Autor: Javier González Pérez
#  Fecha: 25/05/2025
#  Descripción: Script para transformar un archivo JSONL con preguntas de test en un archivo Excel estructurado. 
#  Primero convierte el JSONL a un CSV intermedio, luego agrupa y reorganiza las preguntas por identificador en 
#  columnas separadas para cada pregunta, opciones y respuesta correcta, generando un archivo Excel listo para análisis
#  o uso posterior en benchmarks automatizados.
# ==========================================================

import json
import csv
import pandas as pd

# Archivos de entrada y salida
jsonl_input_file = "output_test_questions_gemini.jsonl"  # Archivo JSONL de entrada
csv_output_file = "converted_questions.csv"  # Archivo CSV intermedio
excel_output_file = "preguntas_gemini.xlsx"  # Archivo Excel final

# Paso 1: Convertir JSONL a CSV
data = []

# Leer el archivo JSONL línea por línea
with open(jsonl_input_file, "r", encoding="utf-8") as file:
    for line in file:
        # Cargar cada línea como un objeto JSON
        record = json.loads(line)
        record_id = record["id"]
        questions = record["questions_output"]
        
        # Procesar cada pregunta
        for question in questions:
            data.append({
                "id": record_id,
                "question": question["question"],
                "options": " | ".join(question["options"]),  # Unir opciones con separador
                "correct_answer": question["correct_answer"]
            })

# Escribir los datos procesados en un archivo CSV
with open(csv_output_file, "w", encoding="utf-8", newline="") as csvfile:
    fieldnames = ["id", "question", "options", "correct_answer"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Escribir encabezados
    writer.writeheader()
    # Escribir filas
    writer.writerows(data)

print(f"Archivo convertido guardado como {csv_output_file}")

# Paso 2: Convertir CSV a Excel con formato transformado
# Leer el archivo CSV
df = pd.read_csv(csv_output_file, delimiter=",", quotechar='"')

# Crear un nuevo DataFrame para el formato esperado
transformed_data = []

# Agrupar las preguntas por 'id'
grouped = df.groupby('id')

for text_id, group in grouped:
    row = {'id': text_id}
    for i, (_, question_row) in enumerate(group.iterrows(), start=1):
        # Agregar las preguntas, opciones y respuestas correctas al formato esperado
        row[f'Q{i}'] = question_row['question']
        row[f'Options_{i}'] = question_row['options']
        row[f'Correct_Option_{i}'] = question_row['correct_answer']
    transformed_data.append(row)

# Convertir los datos transformados en un DataFrame
transformed_df = pd.DataFrame(transformed_data)

# Guardar el DataFrame transformado en un archivo Excel
transformed_df.to_excel(excel_output_file, index=False, engine='openpyxl')

print(f"Archivo transformado guardado en: {excel_output_file}")