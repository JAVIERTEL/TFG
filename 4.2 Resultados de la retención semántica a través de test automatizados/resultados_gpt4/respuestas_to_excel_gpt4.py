# ==========================================================
#  Proyecto: IMPLEMENTACIÓN DE UN SISTEMA DE EVALUACIÓN DE CAPACIDADES DE GRANDES MODELOS DE LENGUAJE A TRAVÉS DE BUCLES DE RESUMEN Y EXTENSIÓN DE TEXTOS
#  Apartado: 4. Resultados
#            4.2 Resultados de la retención semántica a través de test automatizados
#  Autor: Javier González Pérez
#  Fecha: 03/06/2025
#  Descripción: Script para transformar respuestas generadas por ChatGPT-4 desde un archivo JSONL a un archivo Excel 
#  estructurado. Extrae identificadores, tipo de texto, número de pregunta y la respuesta generada de cada entrada, 
#  organizando la información en columnas para facilitar su análisis y procesamiento posterior.
# ==========================================================
import json
import pandas as pd
import re

# Ruta del archivo de entrada y salida
input_file = "benchmark_batch_chat_gpt4_v2-answer.jsonl"
output_file = "respuestas_gpt4_excel.xlsx"

# Lista para almacenar las filas del DataFrame
rows = []

# Procesar línea por línea
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        try:
            entry = json.loads(line)
            custom_id = entry.get("custom_id", "")
            # Extraer el contenido dentro de "response" -> "body" -> "choices" -> "message" -> "content"
            content = (
                entry.get("response", {})
                .get("body", {})
                .get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
                .strip()
            )

            # Extraer campos del custom_id
            match = re.match(r"chat-gpt4--(.+?)--(.+?)--(Q\d+)", custom_id)
            if match:
                tipo_texto = match.group(1)
                id_texto = match.group(2)
                pregunta = match.group(3)

                rows.append({
                    "id": id_texto,
                    "pregunta": pregunta,
                    "tipo_texto": tipo_texto,
                    "respuesta": content
                })
        except json.JSONDecodeError:
            print(f"Error en línea: {line}")

# Crear y guardar el DataFrame
df = pd.DataFrame(rows)
df.to_excel(output_file, index=False)

print(f"Archivo exportado a: {output_file}")