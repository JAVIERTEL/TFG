# ==========================================================
#  Proyecto: IMPLEMENTACIÓN DE UN SISTEMA DE EVALUACIÓN DE CAPACIDADES DE GRANDES MODELOS DE LENGUAJE A TRAVÉS DE BUCLES DE RESUMEN Y EXTENSIÓN DE TEXTOS
#  Apartado: 3. DESARROLLO DEL SISTEMA EXPERIMENTAL
#            3.3 EVALUACIÓN DE LA RETENCIÓN SEMÁNTICA A TRAVÉS DE TEST AUTOMATIZADOS
#  Autor: Javier González Pérez
#  Fecha: 25/05/2025
#  Descripción: Script para evaluar la retención semántica de grandes modelos de lenguaje (LLM) mediante la automatización
#  de tests tipo benchmark. El sistema lee preguntas y textos desde un archivo JSONL, envía las preguntas al modelo Gemini
#  de Google, extrae la respuesta seleccionada (A, B, C o D), y guarda los resultados en un archivo de salida. Incluye 
#  control de cuota de peticiones, manejo de errores y cálculo del porcentaje de respuestas aleatorias.
# ==========================================================
import os
import time
import json
import re
import random
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# 1. Configura tu API Key de Google AI Studio
genai.configure(api_key="")  # 🔒 Sustituye con tu clave real

# 2. Ruta de archivos
input_file = "benchmark_input_gemini.jsonl"
output_file = "benchmark_output_gemini_answers.jsonl"

# 3. Modelo a usar
model = genai.GenerativeModel("gemini-1.5-flash")

# 4. Límite de solicitudes por minuto
REQUESTS_PER_MINUTE = 60

# 5. Cargar IDs ya procesados
def load_processed_ids(path):
    processed = set()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    processed.add(json.loads(line)["custom_id"])
                except:
                    continue
    return processed

# 6. Extraer solo la letra A-D de una respuesta
def extract_letter(response, options=["A", "B", "C", "D"], random_counter=None):
    # Buscar una letra válida en la respuesta
    match = re.search(r"\b([A-D])\b", response.upper())
    if match:
        return match.group(1)
    else:
        # Si no se detecta una respuesta válida, seleccionar una opción aleatoria
        print(f"Respuesta inválida detectada: '{response}'. Seleccionando una opción aleatoria.")
        if random_counter is not None:
            random_counter["count"] += 1
        return random.choice(options)

# 7. Ejecutar las peticiones
def run_benchmark(input_path, output_path):
    processed_ids = load_processed_ids(output_path)
    requests_made = 0
    start_time = time.time()
    total_questions = 0
    random_counter = {"count": 0}  # Contador de respuestas aleatorias

    with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "a", encoding="utf-8") as outfile:
        for line in infile:
            entry = json.loads(line)
            custom_id = entry.get("custom_id")
            if custom_id in processed_ids:
                continue

            try:
                # Extraer contenido
                user_message = next(msg for msg in entry["body"]["messages"] if msg["role"] == "user")
                try:
                    user_data = json.loads(user_message["content"])
                except json.JSONDecodeError:
                    print(f"JSON inválido en {custom_id}")
                    outfile.write(json.dumps({"custom_id": custom_id, "answer": "JSON_ERROR"}, ensure_ascii=False) + "\n")
                    continue

                text = user_data["text"]
                question = user_data["question"]
                options = user_data["options"]

                prompt = (
                    f"{question}\nOptions: {' | '.join(options)}\n\n"
                    f"Text:\n{text}\n\n"
                    f"Answer with only the letter of the correct option (A, B, C, or D)."
                )

                # Llamada a Gemini
                response = model.generate_content(prompt)
                answer_raw = response.text.strip()
                answer = extract_letter(answer_raw, random_counter=random_counter)

                # Guardar resultado
                result = {"custom_id": custom_id, "answer": answer, "raw": answer_raw}
                outfile.write(json.dumps(result, ensure_ascii=False) + "\n")

                total_questions += 1

            except ResourceExhausted:
                print("Cuota alcanzada. Esperando 60 segundos...")
                time.sleep(60)
                continue
            except Exception as e:
                print(f"Error con {custom_id}: {e}")
                outfile.write(json.dumps({"custom_id": custom_id, "answer": "ERROR", "error_detail": str(e)}, ensure_ascii=False) + "\n")

            # Control de RPM
            requests_made += 1
            if requests_made >= REQUESTS_PER_MINUTE:
                elapsed = time.time() - start_time
                if elapsed < 60:
                    time.sleep(60 - elapsed)
                requests_made = 0
                start_time = time.time()

    # Calcular porcentaje de respuestas aleatorias
    random_percentage = (random_counter["count"] / total_questions) * 100 if total_questions > 0 else 0
    print(f"\nPorcentaje de respuestas aleatorias: {random_percentage:.2f}%")

# 8. Ejecutar
if __name__ == "__main__":
    try:
        run_benchmark(input_file, output_file)
        print(f"\nProceso completado. Respuestas guardadas en: {output_file}")
    except KeyboardInterrupt:
        print("\nProceso interrumpido manualmente. Los datos procesados hasta ahora han sido guardados.")