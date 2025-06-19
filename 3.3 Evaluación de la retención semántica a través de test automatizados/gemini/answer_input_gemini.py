# ==========================================================
#  Proyecto: IMPLEMENTACIÓN DE UN SISTEMA DE EVALUACIÓN DE CAPACIDADES DE GRANDES MODELOS DE LENGUAJE A TRAVÉS DE BUCLES DE RESUMEN Y EXTENSIÓN DE TEXTOS
#  Apartado: 3. DESARROLLO DEL SISTEMA EXPERIMENTAL
#            3.3 EVALUACIÓN DE LA RETENCIÓN SEMÁNTICA A TRAVÉS DE TEST AUTOMATIZADOS
#  Autor: Javier González Pérez
#  Fecha: 25/05/2025
#  Descripción: Script para generar un archivo JSONL de benchmark a partir de textos y preguntas almacenados en archivos 
#  Excel. El sistema combina cada texto (en distintas versiones) con sus preguntas asociadas, estructurando cada entrada 
#  para su uso en pruebas automatizadas con el modelo Gemini. Cada entrada incluye el texto, la pregunta, las opciones de
#  respuesta y un identificador único, todo en formato compatible con la API de Gemini.
#
# ==========================================================
import pandas as pd
import json

# Archivos de entrada/salida
texts_file = "textos_gemini.xlsx"  # Archivo Excel con los textos
questions_file = "preguntas_gemini.xlsx"  # Archivo Excel con las preguntas
output_file = "benchmark_batch_gemini.jsonl"  # Archivo JSONL de salida

# Leer los textos desde el archivo Excel
texts_df = pd.read_excel(texts_file)

# Leer las preguntas desde el archivo Excel
questions_df = pd.read_excel(questions_file)

# Asegúrate de que las columnas necesarias existan en ambos archivos Excel
required_text_columns = [
    'id', 'original_text', 'new_text_1_temp_1.0', 'new_text_5_temp_1.0', 'new_text_10_temp_1.0'
]
required_question_columns = [
    'id', 'Q1', 'Options_1', 'Correct_Option_1', 'Q2', 'Options_2', 'Correct_Option_2',
    'Q3', 'Options_3', 'Correct_Option_3', 'Q4', 'Options_4', 'Correct_Option_4',
    'Q5', 'Options_5', 'Correct_Option_5', 'Q6', 'Options_6', 'Correct_Option_6',
    'Q7', 'Options_7', 'Correct_Option_7', 'Q8', 'Options_8', 'Correct_Option_8',
    'Q9', 'Options_9', 'Correct_Option_9', 'Q10', 'Options_10', 'Correct_Option_10'
]

for col in required_text_columns:
    if col not in texts_df.columns:
        raise ValueError(f"El archivo de textos debe contener una columna llamada '{col}'.")
for col in required_question_columns:
    if col not in questions_df.columns:
        raise ValueError(f"El archivo de preguntas debe contener una columna llamada '{col}'.")

# Crear el archivo JSONL de salida
with open(output_file, "w", encoding="utf-8") as jsonl_file:
    for _, text_row in texts_df.iterrows():
        text_id = text_row['id']

        # Iterar sobre las 4 iteraciones del texto
        for iteration_key in ['original_text', 'new_text_1_temp_1.0', 'new_text_5_temp_1.0', 'new_text_10_temp_1.0']:
            text = text_row[iteration_key]

            # Filtrar las preguntas correspondientes al texto actual
            question_rows = questions_df[questions_df['id'] == text_id]

            # Iterar sobre las preguntas generadas
            for _, question_row in question_rows.iterrows():
                for i in range(1, 11):  # Procesar hasta Q10
                    question_key = f"Q{i}"
                    options_key = f"Options_{i}"
                    
                    # Verificar si la pregunta y las opciones existen
                    if pd.isna(question_row.get(question_key)) or pd.isna(question_row.get(options_key)):
                        continue
                    
                    question = question_row[question_key]
                    options = question_row[options_key].split(", ")  # Separar las opciones por coma y espacio
                    
                    # Crear el ID del batch
                    custom_id = f"gemini--{iteration_key}--{text_id}--{question_key}"

                    # Crear la estructura del JSONL para la API
                    jsonl_entry = {
                        "custom_id": custom_id,
                        "method": "POST",
                        "url": "/v1beta/models/gemini-1.5-flash:generateContent",  # Endpoint de Gemini
                        "body": {
                            "model": "gemini-1.5-flash",  # Modelo Gemini
                            "messages": [
                                {
                                    "role": "system",
                                    "content": (
                                        "Answer the multiple-choice question based solely on the content of the text. "
                                        "You cannot use any information beyond what is in the text. Respond exclusively with the letter of the answer."
                                    )
                                },
                                {
                                    "role": "user",
                                    "content": json.dumps({
                                        "text": text.replace('"', "'"),  # Reemplazar comillas dobles por simples
                                        "question": question,
                                        "options": options
                                    })
                                }
                            ]
                        }
                    }

                    # Escribir la entrada en el archivo JSONL
                    jsonl_file.write(json.dumps(jsonl_entry) + "\n")

print(f"Archivo JSONL generado correctamente: {output_file}")