# TFG – Evaluación de la fidelidad semántica en LLMs mediante bucles de resumen y expansión

Este repositorio contiene el código fuente y la documentación asociada al Trabajo de Fin de Grado titulado **“Implementación de un sistema de evaluación de capacidades de Grandes Modelos de Lenguaje a través de bucles de resumen y extensión de textos”**.  
El proyecto analiza cómo la información original se degrada o se conserva al someterse a procesos iterativos de compresión y expansión, utilizando modelos como GPT-4 Mini y Gemini 1.5 Flash.  

## Estructura del repositorio

La estructura del proyecto sigue el esquema del documento del TFG y se organiza en carpetas numeradas por sección:

### `3.1 Desarrollo de los bucles de resumen y expansión`
Contiene scripts para ejecutar iteraciones de resumen y expansión sobre los textos del dataset CNN/DailyMail, utilizando Groq, OpenAI (GPT-4 Mini) y Gemini.

📁 Ver ficheros asociados en Google Drive:  
[📂 Excel y JSONL de resultados 3.1](https://drive.google.com/drive/folders/16aFghI1WKmBDqHC1oyrd7UaQJRghRKBW)

---

### `3.2 Implementación del sistema de evaluación automática`
Incluye el código encargado de evaluar los textos generados utilizando métricas ROUGE y BERTScore, almacenando los resultados en Excel.

📁 Ver ficheros asociados en Google Drive:  
[📂 Excel de resultados 3.2](https://drive.google.com/drive/folders/10WGDmhASPoI1lv_OGez5CkUPlyEd-4TA)

---

### `3.3 Evaluación de la retención semántica a través de test automatizados`

#### Subcarpeta `gemini`
Generación de preguntas tipo test, envío de respuestas y análisis de comprensión utilizando el modelo Gemini.

📁 Ver ficheros asociados en Google Drive:  
[📂 Excel y JSONL para Gemini 3.3](https://drive.google.com/drive/folders/1ccwOUOaXPn6yKV580AL0S86Pct_RFy9o)

#### Subcarpeta `gpt4`
Benchmark equivalente aplicado sobre GPT-4 Mini.

📁 Ver ficheros asociados en Google Drive:  
[📂 Excel y JSONL para GPT-4 3.3](https://drive.google.com/drive/folders/1Ox28iNqlJ3ftdcZLCcHMAQPfhQtW-zZ8)

---

### `4.1 Representación gráfica de métricas ROUGE y BERTScore`
Script para generación de gráficas de evolución de precisión, recall y F1 a lo largo de las iteraciones de los modelos.

📁 Ver gráficas exportadas:  
[📂 Drive gráficas 4.1](https://drive.google.com/drive/folders/1zzASjMhB4kRCQNj8nDZHpPyGEH7oQcQu)

---

### `4.2 Evaluación mediante test sobre textos resumidos y expandidos`

#### Subcarpeta `gemini`
Análisis del rendimiento de Gemini respondiendo preguntas tipo test a partir de sus propias versiones del texto.

📁 Ver ficheros asociados:  
[📂 Excel y Gráficas 4.2 Gemini](https://drive.google.com/drive/folders/1bJIm1KqMzbc7emJR3zV-Ix6m8g4Ef4aQ)

#### Subcarpeta `gpt4`
Mismo análisis con el modelo GPT-4 Mini.

📁 Ver ficheros asociados:  
[📂 Excel yGráficas 4.2 GPT-4](https://drive.google.com/drive/folders/1bJIm1KqMzbc7emJR3zV-Ix6m8g4Ef4aQ)

---

## Licencia

Este repositorio está licenciado bajo la licencia MIT. Puedes consultar el archivo [`LICENSE`](./LICENSE) para más información.

---

## Autor

**Javier González Pérez**  
Grado en Ingeniería de Tecnologías y Servicios de Telecomunicación  
Universidad Politécnica de Madrid (ETSIT)  
2025

---

## Contacto

📧 javierlaguna2001@gmail.com 
🔗 [GitHub – @JAVIERTEL](https://github.com/JAVIERTEL)
