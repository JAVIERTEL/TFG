# ==========================================================
#  Proyecto: IMPLEMENTACIÓN DE UN SISTEMA DE EVALUACIÓN DE CAPACIDADES DE GRANDES MODELOS DE LENGUAJE A TRAVÉS DE BUCLES DE RESUMEN Y EXTENSIÓN DE TEXTOS
#  Apartado: 3. DESARROLLO DEL SISTEMA EXPERIMENTAL
#            3.4 GENERACIÓN DE ARCHIVOS JSONL PARA SOLICITUDES MASIVAS DE PREGUNTAS TIPO TEST
#  Autor: Javier González Pérez
#  Fecha: 15/05/2025
#  Descripción: Este script convierte textos originales de un archivo Excel en entradas JSONL estructuradas para realizar solicitudes POST
#               al endpoint /v1/chat/completions, generando preguntas tipo test con formato validado mediante un esquema JSON.
# ==========================================================


import pandas as pd
import json

# Ruta del archivo de entrada y salida
input_file = "textos_gemini.xlsx"  # Archivo con los textos originales de CNN
output_file = " batch_input_test_questions_gpt4.jsonl"  # Archivo de salida en formato JSONL

# Leer los textos originales desde el archivo Excel
df = pd.read_excel(input_file)

# Asegúrate de que la columna con los textos se llama 'original_text'
if 'original_text' not in df.columns:
    raise ValueError("El archivo debe contener una columna llamada 'original_text'.")

# Abrir el archivo JSONL para escritura
with open(output_file, "w", encoding="utf-8") as jsonl_file:
    for index, row in df.iterrows():
        # Obtener el texto original
        original_text = row['original_text']
        id = row['id']
        
        # Crear la estructura del JSONL según el formato solicitado
        jsonl_entry = {
            "custom_id": f"{id}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o-mini-2024-07-18",
                "messages": [
                    {
                        "role": "system",
                        "content": "Generate 10 multiple-choice questions based on the following text. "
                        "Each question should have four answer options (A, B, C, and D), with only one correct answer. "
                        "Clearly indicate the correct answer in each case. Ensure that the questions cover different aspects "
                        "of the text, including facts, dates, relevant data, and implicit information when possible. Keep the questions clear and concise."
                    },
                    {
                        "role": "user",
                        "content": original_text
                    }
                ],
                "response_format": {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "ten_test_qa",
                        "strict": True,  # Corregido a Python True
                        "schema": {
                            "type": "object",
                            "required": ["questions"],
                            "properties": {
                                "questions": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "required": ["question", "options", "correct_answer"],
                                        "properties": {
                                            "options": {
                                                "type": "array",
                                                "items": {
                                                    "type": "string",
                                                    "description": "One of the four possible answer choices."
                                                }
                                            },
                                            "question": {
                                                "type": "string",
                                                "description": "The text of the multiple-choice question."
                                            },
                                            "correct_answer": {
                                                "enum": ["A", "B", "C", "D"],
                                                "type": "string",
                                                "description": "The correct answer option (A, B, C, or D)."
                                            }
                                        },
                                        "additionalProperties": False  # Corregido a Python False
                                    }
                                }
                            },
                            "additionalProperties": False  # Corregido a Python False
                        }
                    }
                },
                "max_tokens": 10000
            }
        }
        
        # Escribir la entrada en el archivo JSONL - json.dumps convertirá True/False de Python a true/false en JSON
        jsonl_file.write(json.dumps(jsonl_entry) + "\n")

print(f"Archivo JSONL generado: {output_file}")
