# 4.2 Evaluación de respuestas generadas por Gemini

Este módulo contiene los scripts utilizados para evaluar la capacidad del modelo Gemini 1.5 Flash al responder preguntas tipo test generadas a partir de textos originales, resumidos y expandidos. Los resultados permiten analizar la retención semántica del modelo sobre diferentes versiones de los textos procesados.

## Estructura

Los siguientes scripts están incluidos:

- `representacion_resultados_gemini.py`: genera gráficos comparativos de aciertos para las distintas versiones del texto por iteración.
- `respuestas_to_excel_gemini.py`: transforma las respuestas generadas por Gemini desde un archivo JSONL a formato Excel para facilitar su análisis.
- `resultados_gemini.py`: calcula métricas de evaluación como porcentaje de aciertos, distribución de respuestas y tasa de fallback (respuestas aleatorias), comparando las respuestas del modelo frente a las correctas.

## Archivos de entrada requeridos

Los archivos necesarios para ejecutar los scripts están disponibles en el siguiente enlace de Google Drive:

📁 **[Archivos de entrada (Excel y JSONL)](https://drive.google.com/drive/folders/1bJIm1KqMzbc7emJR3zV-Ix6m8g4Ef4aQ)**

Asegúrate de colocar los archivos en el mismo directorio donde se ejecutan los scripts o adaptar las rutas de lectura.

## Requisitos

Este módulo utiliza las siguientes bibliotecas de Python:

- `pandas`
- `matplotlib`
- `openpyxl`
- `json`
- `os`, `re`

Puedes instalarlas con:

```bash
pip install pandas matplotlib openpyxl
```

## Salidas

- Archivos `.xlsx` con los resultados estructurados.
- Gráficos de evaluación exportados en formato `.png`.

## Uso

Ejecuta los scripts en el orden indicado. Por ejemplo:

```bash
python respuestas_to_excel_gemini.py
python resultados_gemini.py
python representacion_resultados_gemini.py
```

## Autor

Javier González Pérez  
Trabajo de Fin de Grado — UPM 2025
