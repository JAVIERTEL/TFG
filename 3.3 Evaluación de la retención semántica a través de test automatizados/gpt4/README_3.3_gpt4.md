# Evaluación de Retención Semántica mediante Preguntas Tipo Test — GPT-4

Este módulo contiene los scripts necesarios para generar, transformar y evaluar automáticamente preguntas tipo test utilizando textos procesados por el modelo **GPT-4 Mini**. Se trata de una parte del sistema de evaluación iterativa de modelos de lenguaje, centrada en medir la fidelidad semántica y de comprensión tras procesos de resumen y expansión textual.

---

## 🧠 Objetivo

Evaluar la capacidad de comprensión de **GPT-4 Mini** sobre versiones modificadas de los textos (original, resumida, expandida) mediante generación y resolución automatizada de tests.

---

## 📂 Estructura de archivos

### Scripts incluidos

- `generación_preguntas_test_gpt4.py`: genera preguntas de opción múltiple a partir de textos usando GPT-4 Mini mediante API.
- `json_output_to_excel_gpt4.py`: transforma las respuestas generadas en formato JSONL a un archivo Excel estructurado.
- `benchmark_input_gpt4.py`: genera el archivo JSONL con combinaciones de preguntas y versiones del texto para evaluación.
- `respuestas_to_excel_gpt4.py`: transforma las respuestas del modelo a formato Excel para su análisis.
- `representacion_resultados_gpt-4.py`: representa gráficamente la precisión del modelo en cada nivel de resumen y expansión.
- `resultados_gpt-4.py`: calcula métricas globales de rendimiento del modelo a partir de las respuestas generadas.

---

## 📁 Archivos de datos

Debido al tamaño de los ficheros `.jsonl` y `.xlsx`, estos se han alojado externamente en Google Drive. Puedes acceder a ellos aquí:

📎 [Google Drive - Archivos GPT-4](https://drive.google.com/drive/folders/1Ox28iNqlJ3ftdcZLCcHMAQPfhQtW-zZ8)

Incluye:
- `questions_output_1000.xlsx`: preguntas generadas a partir del texto original.
- `output_gpt4-mini_1000.xlsx`: versiones resumidas y expandidas de los textos originales con GPT-4 Mini.
- `benchmark_input_answer_gpt4.jsonl`: benchmark preparado para evaluación automática.
- `answers_gpt4_output.jsonl`: respuestas del modelo a cada combinación texto-pregunta.
- `questions_transformadas_gpt4.xlsx`: preguntas convertidas a un formato tabular para análisis posterior.

---

## ▶️ Uso básico

1. **Generar preguntas**:
   ```bash
   python generación_preguntas_test_gpt4.py
   ```

2. **Convertir JSONL a Excel**:
   ```bash
   python json_output_to_excel_gpt4.py
   ```

3. **Preparar benchmark de evaluación**:
   ```bash
   python benchmark_input_gpt4.py
   ```

4. **Transformar respuestas del modelo a Excel**:
   ```bash
   python respuestas_to_excel_gpt4.py
   ```

5. **Visualizar resultados**:
   ```bash
   python representacion_resultados_gpt-4.py
   ```

6. **Calcular métricas agregadas**:
   ```bash
   python resultados_gpt-4.py
   ```

---

## 📄 Licencia

Este proyecto está licenciado bajo los términos de la **Licencia MIT**, lo que permite su uso, modificación y distribución con atribución adecuada.

---

## ✍️ Autor

Javier González Pérez  
[Repositorio principal del TFG](https://github.com/JAVIERTEL/TFG)
