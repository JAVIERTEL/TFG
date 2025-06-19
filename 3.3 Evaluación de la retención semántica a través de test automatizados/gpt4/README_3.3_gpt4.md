# Evaluación de Retención Semántica mediante Preguntas Tipo Test — GPT-4

Este módulo contiene los scripts necesarios para generar, transformar y evaluar automáticamente preguntas tipo test utilizando textos procesados por el modelo GPT-4 Mini. Se trata de una parte del proyecto de evaluación iterativa de modelos de lenguaje, centrada en medir la fidelidad semántica y de comprensión tras cada iteración de resumen y expansión.

---

## 🧠 Objetivo

Evaluar la capacidad de comprensión de GPT-4 Mini sobre versiones modificadas de textos (originales, resumidos, expandidos) mediante generación y resolución automatizada de tests.

---

## 📂 Estructura de archivos

### Scripts incluidos

- `generación_preguntas_test_gpt4.py`: genera preguntas de opción múltiple a partir de textos usando GPT-4 Mini mediante API.
- `json_output_to_excel_gpt4.py`: transforma las respuestas generadas (en formato JSONL) a Excel estructurado.
- `answer_input_gpt4.py`: genera el archivo JSONL con combinaciones de preguntas + textos para evaluar.
- `answer_gpt4_output.py`: evalúa las respuestas del modelo sobre textos modificados y almacena resultados.

---

## 📁 Archivos de datos

Debido al tamaño de los ficheros (`.jsonl` y `.xlsx`), estos no están en este repositorio. Puedes encontrarlos en el siguiente enlace de Google Drive:

📎 [Google Drive - Archivos GPT-4](https://drive.google.com/drive/folders/1Ox28iNqlJ3ftdcZLCcHMAQPfhQtW-zZ8)

Incluyen:
- `questions_output_1000.xlsx`: Preguntas generadas desde el texto original.
- `output_gpt4-mini_1000.xlsx`: Textos procesados con GPT-4 Mini.
- `benchmark_input_answer_gpt4.jsonl`: Benchmark de entrada para evaluación.
- `answers_gpt4_output.jsonl`: Respuestas del modelo a las preguntas.
- `questions_transformadas_gpt4.xlsx`: Preguntas en formato tabular para evaluación.

---

## ▶️ Uso básico

1. **Generar preguntas**:
   ```bash
   python generación_preguntas_test_gpt4.py
   ```

2. **Convertir a Excel**:
   ```bash
   python json_output_to_excel_gpt4.py
   ```

3. **Preparar benchmark**:
   ```bash
   python answer_input_gpt4.py
   ```

4. **Evaluar respuestas**:
   ```bash
   python answer_gpt4_output.py
   ```

---

## 📄 Licencia

MIT License — libre para uso, distribución y modificación con atribución.

---

## ✍️ Autor

Javier González Pérez  
[Repositorio principal del TFG](https://github.com/JAVIERTEL/TFG)