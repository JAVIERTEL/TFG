# 📊 Evaluación de respuestas generadas - GPT-4

Este directorio forma parte del sistema desarrollado para evaluar la retención de información semántica por parte de modelos LLM, comparando respuestas generadas por GPT-4 frente a una batería de preguntas tipo test generadas a partir de los textos originales.

## 🧩 Estructura de scripts

- `respuestas_to_excel_gpt4.py`: Extrae las respuestas generadas por GPT-4 desde un archivo `.jsonl` (`benchmark_batch_chat_gpt4_v2-answer.jsonl`) y las transforma en una tabla Excel estructurada, con columnas para `id`, `pregunta`, `tipo_texto` y `respuesta`.
- `resultados_gpt-4.py`: Compara las respuestas generadas por GPT-4 con las respuestas correctas de referencia, determinando si son correctas, incorrectas o inválidas. El resultado se guarda en `resultados_gpt4.xlsx`.
- `representacion_resultados_gpt-4.py`: Genera visualizaciones gráficas de los resultados de evaluación, mostrando el rendimiento de GPT-4 en distintas versiones del texto (original, resumido y expandido) por iteraciones.

## 🗂️ Archivos necesarios (no incluidos en este repositorio)

Los ficheros de entrada y salida se encuentran en el siguiente enlace de Zenodo:

🔗 [Excel y Gráfica – Resultados GPT-4](https://doi.org/10.5281/zenodo.15714532)


## ✍️ Autor

Javier González Pérez · Trabajo Fin de Grado - UPM

---

### Licencia

Este proyecto está licenciado bajo la licencia MIT. Puedes consultar los términos completos [aquí](https://opensource.org/licenses/MIT).
