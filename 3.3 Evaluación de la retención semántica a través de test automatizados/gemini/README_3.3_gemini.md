# 3.3 Evaluación de la retención semántica (Gemini)

Esta carpeta contiene los scripts necesarios para evaluar la capacidad del modelo Gemini para retener información semántica tras la generación iterativa de textos (resumen y expansión). El sistema se basa en la generación de preguntas tipo test a partir del texto original y la evaluación de las respuestas del modelo sobre las distintas versiones del texto generado.

## Estructura

### Scripts incluidos

- `generación_preguntas_test_gemini.py`: genera 10 preguntas tipo test a partir de un texto dado usando Gemini. Envía solicitudes en formato JSONL a la API de Google Generative AI.
- `json_output_to_excel_gemini.py`: transforma las preguntas generadas en formato JSONL a formato tabular Excel, reestructurando los datos para facilitar su análisis.
- `answer_input_gemini.py`: genera las combinaciones de preguntas y versiones de texto (original, resumen y expansión) para construir un benchmark de evaluación.
- `answer_gemini_output.py`: envía las combinaciones generadas al modelo Gemini y almacena las respuestas, normalizando el formato y manejando errores.

### Flujo de trabajo

1. **Generación de preguntas** a partir del texto original (`generación_preguntas_test_gemini.py`).
2. **Conversión a Excel** del archivo JSONL con las preguntas (`json_output_to_excel_gemini.py`).
3. **Creación del benchmark de evaluación** combinando preguntas y textos (`answer_input_gemini.py`).
4. **Evaluación automática de respuestas** generadas por Gemini (`answer_gemini_output.py`).

## Estructura esperada de archivos

Los siguientes ficheros de datos están disponibles en Google Drive y deben ser descargados para ejecutar correctamente los scripts:

📂 [Archivos Gemini (Excel y JSONL)](https://doi.org/10.5281/zenodo.15714532)

## Requisitos

- Python 3.9+
- Bibliotecas:
  - `pandas`
  - `openpyxl`
  - `google.generativeai`
  - `tqdm`
  - `json`, `re`, `time`

## Uso

1. Ejecuta `generación_preguntas_test_gemini.py` para obtener preguntas tipo test.
2. Transforma el resultado con `json_output_to_excel_gemini.py`.
3. Crea el archivo de benchmark con `answer_input_gemini.py`.
4. Evalúa las respuestas con `answer_gemini_output.py`.
