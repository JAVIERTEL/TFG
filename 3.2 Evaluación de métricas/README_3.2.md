# 3.2 Evaluación de métricas automáticas

Este módulo implementa un sistema para evaluar cuantitativamente la fidelidad de los textos generados por modelos LLM, comparando sus resúmenes y expansiones frente al texto original. Se aplican métricas automáticas ampliamente utilizadas en NLP como **ROUGE-1** y **BERTScore**, organizando los resultados en un archivo Excel estructurado por hojas.

## 📂 Archivos incluidos

- `implementacion_v3.py`: script principal que calcula métricas entre textos (original, resumen, expansión) y guarda los resultados en un Excel.
- Archivos de datos asociados disponibles en Zenodo:  
  🔗 (https://doi.org/10.5281/zenodo.15714532)

## ⚙️ Funcionalidades

- **Lectura del dataset** desde un archivo Excel que contiene textos originales y versiones generadas.
- **Comparación por lotes** mediante ROUGE-1 y BERTScore para tres escenarios:
  - Texto original vs resúmenes generados.
  - Texto original vs textos expandidos.
  - Resumen humano vs resúmenes generados.
- **Similitud léxica adicional** con TF-IDF (comentada en algunas ejecuciones).
- **Escritura de resultados** en hojas separadas de un único archivo Excel (`textos_gemini_stats.xlsx`), listas para análisis posterior.

## 📊 Ejemplo de hojas de resultados generadas

- `orig_txt-summ_ROUGE_temp1.0`: ROUGE entre original y resumen.
- `orig_txt-txts_BERT_temp1.0`: BERTScore entre original y textos generados.
- `orig_txt-summ_TFIDF_temp1.0`: similitud TF-IDF entre original y resumen.

## 🧠 Requisitos

- Python 3.x
- Paquetes: `pandas`, `rouge-score`, `bert-score`, `scikit-learn`, `openpyxl`

Instalación rápida:

```bash
pip install pandas rouge-score bert-score scikit-learn openpyxl
```

## 📌 Notas

- El sistema evita duplicados revisando los IDs ya procesados en el Excel de salida.
- Si el archivo `textos_gemini_stats.xlsx` ya existe, se añade información incrementalmente.
- Las versiones generadas por los modelos se identifican con sufijos como `summary_1_temp_1.0`, `new_text_3_temp_1.0`, etc.

## 📄 Licencia

MIT License – ver archivo raíz del repositorio para más detalles.
