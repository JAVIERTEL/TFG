# 4.2 Evaluación de respuestas generadas por Gemini

Este directorio contiene los scripts utilizados para evaluar la capacidad de retención semántica del modelo **Gemini-1.5-Flash** mediante preguntas tipo test. El proceso evalúa si el modelo puede responder correctamente a preguntas generadas a partir del texto original cuando se le presentan distintas versiones del mismo (original, resumida, expandida).

## Scripts incluidos

- **`answer_input_gemini.py`**: Genera entradas JSONL que contienen preguntas y diferentes versiones del texto para ser enviadas a la API de Gemini.
- **`answer_gemini_output.py`**: Envía las entradas generadas al modelo Gemini, recoge las respuestas, controla la tasa de peticiones y normaliza el formato.
- **`respuestas_to_excel_gemini.py`**: Convierte el archivo JSONL con respuestas en un archivo Excel organizado por texto, pregunta y tipo de versión textual.
- **`resultados_gemini.py`**: Compara las respuestas generadas con las respuestas correctas para determinar su grado de acierto.

## Datos de entrada

Los archivos de entrada necesarios (JSONL y Excel) están disponibles en el siguiente enlace de Google Drive:

🔗 [Archivos de entrada y preguntas generadas](https://drive.google.com/drive/folders/1bJIm1KqMzbc7emJR3zV-Ix6m8g4Ef4aQ)

## Estructura esperada

- `responses_gemini_answers.jsonl`: respuestas del modelo Gemini.
- `preguntas_gemini_transformado.xlsx`: contiene las 10 preguntas por texto con sus opciones y respuestas correctas.
- `respuestas_gemini_excel.xlsx`: respuestas generadas procesadas.
- `resultados_gemini.xlsx`: resultado final con evaluación de aciertos.

## Resultado final

El resultado final del análisis se encuentra en el siguiente enlace:

📊 [Resultados finales en Excel y visualizaciones](https://drive.google.com/drive/folders/1zzASjMhB4kRCQNj8nDZHpPyGEH7oQcQu)