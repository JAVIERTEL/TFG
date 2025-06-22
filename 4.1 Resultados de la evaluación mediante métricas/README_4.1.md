
# 📊 Visualización de Resultados: Evaluación de Modelos LLM

Este módulo forma parte del apartado **4.1 Resultados de la evaluación mediante métricas** del TFG *"Implementación de un sistema de evaluación de capacidades de grandes modelos de lenguaje a través de bucles de resumen y extensión de textos"*. El objetivo principal es analizar la evolución de métricas (ROUGE y BERTScore) a lo largo de iteraciones de resumen/expansión, comparando diferentes modelos LLM como GPT-4 Mini y Gemini.

## 📁 Archivos incluidos

- `graficas_comparativas_llm.py`: Script principal para:
  - Leer métricas desde archivos Excel.
  - Transformar los datos para visualizar por iteración y métrica.
  - Generar gráficos de líneas con barras de error (precision, recall, F1).
  - Comparar modelos mediante gráficos de barras agrupadas.

## 📂 Datos de entrada

Los datos deben estar previamente generados en formato Excel a partir de los experimentos con los modelos. En este caso, se incluyen:

🔗 [https://doi.org/10.5281/zenodo.15714532](https://doi.org/10.5281/zenodo.15714532)

Archivos utilizados:
- `textos_gpt4_stats.xlsx` – métricas de evaluación del modelo GPT-4 Mini  
- `textos_gemini_stats.xlsx` – métricas de evaluación del modelo Gemini 1.5 Flash


## 📈 Salida

Las gráficas generadas se guardan automáticamente en la carpeta [`graficas_finales/`](https://drive.google.com/drive/folders/1zzASjMhB4kRCQNj8nDZHpPyGEH7oQcQu) e incluyen:

- Evolución de precision, recall y F1 a lo largo de iteraciones.
- Comparativa entre modelos para iteraciones clave (1, 5, 10).

## ▶️ Ejecución

```bash
python graficas_comparativas_llm.py
```

## 📋 Requisitos

- Python 3.8+
- pandas
- matplotlib
- seaborn
- openpyxl

Puedes instalar los requisitos con:

```bash
pip install -r requirements.txt
```

## 📄 Licencia

MIT License
