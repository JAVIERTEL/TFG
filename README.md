# TFG – IMPLEMENTACIÓN DE UN SISTEMA DE EVALUACIÓN DE CAPACIDADES DE GRANDES MODELOS DE LENGUAJE A TRAVÉS DE BUCLES DE RESUMEN Y EXTENSIÓN DE TEXTOS

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15714532.svg)](https://doi.org/10.5281/zenodo.15714532)

Este repositorio contiene el código fuente y la documentación asociada al Trabajo de Fin de Grado titulado **“Implementación de un sistema de evaluación de capacidades de Grandes Modelos de Lenguaje a través de bucles de resumen y extensión de textos”**.  
El proyecto analiza cómo la información original se degrada o se conserva al someterse a procesos iterativos de compresión y expansión, utilizando modelos como GPT-4 Mini y Gemini 1.5 Flash.  

Todos los archivos complementarios utilizados (Excel, JSONL, resultados y gráficas) han sido depositados y están disponibles en Zenodo:  
📁 [Ver y descargar material completo (Zenodo)](https://doi.org/10.5281/zenodo.15714532)

---

## Estructura del repositorio

La estructura del proyecto sigue el esquema del documento del TFG y se organiza en carpetas numeradas por sección:

### `3.1 Desarrollo de los bucles de resumen y expansión`
Contiene scripts para ejecutar iteraciones de resumen y expansión sobre los textos del dataset CNN/DailyMail, utilizando Groq, OpenAI (GPT-4 Mini) y Gemini.

---

### `3.2 Implementación del sistema de evaluación automática`
Incluye el código encargado de evaluar los textos generados utilizando métricas ROUGE y BERTScore, almacenando los resultados en Excel.

---

### `3.3 Evaluación de la retención semántica a través de test automatizados`

#### Subcarpeta `gemini`
Generación de preguntas tipo test, envío de respuestas y análisis de comprensión utilizando el modelo Gemini.

#### Subcarpeta `gpt4`
Benchmark equivalente aplicado sobre GPT-4 Mini.

---

### `4.1 Representación gráfica de métricas ROUGE y BERTScore`
Script para generación de gráficas de evolución de precisión, recall y F1 a lo largo de las iteraciones de los modelos.

---

### `4.2 Evaluación mediante test sobre textos resumidos y expandidos`

#### Subcarpeta `gemini`
Análisis del rendimiento de Gemini respondiendo preguntas tipo test a partir de sus propias versiones del texto.

#### Subcarpeta `gpt4`
Mismo análisis con el modelo GPT-4 Mini.

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
