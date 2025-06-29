# ==========================================================
#  Proyecto: IMPLEMENTACIÓN DE UN SISTEMA DE EVALUACIÓN DE CAPACIDADES DE GRANDES MODELOS DE LENGUAJE A TRAVÉS DE BUCLES DE RESUMEN Y EXTENSIÓN DE TEXTOS
#  Apartado: 4. Resultados
#            4.2 Resultados de la retención semántica a través de test automatizados
#  Autor: Javier González Pérez
#  Fecha: 03/06/2025
#  Descripción: Script para transformar respuestas generadas por Gemini desde un archivo JSONL a un archivo Excel 
#  estructurado. Extrae identificadores, tipo de texto, número de pregunta y la respuesta original de cada entrada, 
#  organizando la información en columnas para facilitar su análisis y procesamiento posterior.
# ==========================================================
import json
import pandas as pd
import re

# Ruta del archivo de entrada y salida
input_file = "anwer_gemini_output.jsonl"
output_file = "respuestas_gemini_excel.xlsx"

# Lista para almacenar las filas del DataFrame
rows = []

# Procesar línea por línea
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        try:
            entry = json.loads(line)
            custom_id = entry.get("custom_id", "")
            raw = entry.get("raw", "").strip()

            # Extraer campos del custom_id
            match = re.match(r"gemini--(.+?)--(.+?)--(Q\d+)", custom_id)
            if match:
                tipo_texto = match.group(1)
                id_texto = match.group(2)
                pregunta = match.group(3)

                rows.append({
                    "id": id_texto,
                    "pregunta": pregunta,
                    "tipo_texto": tipo_texto,
                    "respuesta": raw
                })
        except json.JSONDecodeError:
            print(f"Error en línea: {line}")

# Crear y guardar el DataFrame
df = pd.DataFrame(rows)
df.to_excel(output_file, index=False)

print(f"Archivo exportado a: {output_file}")
