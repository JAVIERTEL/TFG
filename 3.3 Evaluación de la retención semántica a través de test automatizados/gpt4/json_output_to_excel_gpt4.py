# ==========================================================
#  Proyecto: IMPLEMENTACIÓN DE UN SISTEMA DE EVALUACIÓN DE CAPACIDADES DE GRANDES MODELOS DE LENGUAJE A TRAVÉS DE BUCLES DE RESUMEN Y EXTENSIÓN DE TEXTOS
#  Apartado: 3. DESARROLLO DEL SISTEMA EXPERIMENTAL
#            3.3 EVALUACIÓN DE LA RETENCIÓN SEMÁNTICA A TRAVÉS DE TEST AUTOMATIZADOS
#  Autor: Javier González Pérez
#  Fecha: 15/05/2025
#  Descripción: Script para transformar un archivo JSONL con respuestas generadas por un modelo de lenguaje en un archivo 
#  Excel estructurado. Extrae, para cada registro, el identificador, las preguntas, opciones y respuestas correctas, 
#  organizando la información en columnas separadas para facilitar su análisis o reutilización en procesos de evaluación 
#  automatizada.
# ==========================================================
import json
import pandas as pd

# Ruta del archivo JSONL de entrada y el archivo Excel de salida
input_file = "batch_output_test_questions_gemini.jsonl"
output_file = "questions_gpt4.xlsx"

# Lista para almacenar los datos procesados
data = []

# Leer el archivo JSONL línea por línea
with open(input_file, "r", encoding="utf-8") as jsonl_file:
    for line in jsonl_file:
        # Cargar la línea como un objeto JSON
        entry = json.loads(line)
        
        # Extraer el custom_id
        custom_id = entry.get("custom_id", "")
        
        # Extraer las preguntas y opciones del cuerpo de la respuesta
        choices = entry.get("response", {}).get("body", {}).get("choices", [])
        if choices:
            content = choices[0].get("message", {}).get("content", "")
            try:
                # Deserializar el contenido si es una cadena JSON
                questions = json.loads(content).get("questions", [])
            except json.JSONDecodeError:
                print(f"Error al decodificar el contenido JSON en custom_id: {custom_id}")
                questions = []
        else:
            questions = []
        
        # Crear un diccionario para almacenar las columnas de este registro
        row = {"id": custom_id}
        
        # Procesar cada pregunta y sus opciones
        for i, question in enumerate(questions, start=1):
            row[f"Q{i}"] = question.get("question", "")
            row[f"Options_{i}"] = ", ".join(question.get("options", []))
            row[f"Correct_Option_{i}"] = question.get("correct_answer", "")
        
        # Añadir la fila a los datos
        data.append(row)

# Crear un DataFrame de pandas con los datos procesados
df = pd.DataFrame(data)

# Guardar el DataFrame en un archivo Excel
df.to_excel(output_file, index=False)

print(f"Archivo Excel generado: {output_file}")
