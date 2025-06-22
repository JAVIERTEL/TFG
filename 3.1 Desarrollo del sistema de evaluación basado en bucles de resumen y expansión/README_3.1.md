# 🌀 3.1 Desarrollo del sistema de evaluación basado en bucles de resumen y expansión

Este apartado contiene los scripts utilizados para implementar el sistema experimental basado en la generación iterativa de resúmenes y expansiones de texto mediante diferentes LLMs.

## 📁 Contenido de la carpeta

### 1. `Descarga_textos.py`
Script que permite descargar textos y resúmenes del dataset **CNN/DailyMail** usando la API de Hugging Face. Cada entrada incluye:
- Texto original (`article`)
- Resumen humano (`highlights`)
- Cálculo de longitud en palabras
- Almacenamiento en un archivo Excel

🔗 Dataset usado: [`abisee/cnn_dailymail`](https://huggingface.co/datasets/abisee/cnn_dailymail)

---

### 2. `bucle_resumen_expansion_groq.py`
Script que implementa un bucle de 10 iteraciones de resumen y expansión usando el modelo **LLaMA-3.2-1b-preview** desde la API de **Groq**.

- Lee textos desde un Excel
- Resume y expande de forma recursiva
- Guarda los resultados en otro Excel
- Controla errores de API y permite reinicio

---

### 3. `bucles_resumen_expansion_gpt4.py`
Versión equivalente del sistema para el modelo **GPT-4o Mini** accedido mediante la plataforma **OpenRouter** y la librería `openai`.

- Adapta el mismo flujo para el cliente OpenAI
- Usa prompts con mensajes `system` y `user`
- Exporta los resultados por hoja en un archivo Excel

---

### 4. `bucle_resumen_expansion_gemini.py`
Adaptación del sistema de resumen-expansión para el modelo **Gemini-1.5-Flash**, mediante la API de Google Generative AI.

- Utiliza la librería `google.generativeai`
- Integra control de cuota por RPM (peticiones por minuto)
- Añade manejo de errores y control de respuesta

---

## 🧪 Objetivo del sistema

Explorar la retención de información a través de generación iterativa:
- 🧩 ¿Se conserva el contenido original tras varios ciclos de resumen y expansión?
- 🔁 ¿Cómo difiere este comportamiento entre modelos?

Cada script puede ejecutarse de forma independiente, y los resultados pueden integrarse en las evaluaciones posteriores (análisis de métricas y preguntas tipo test).

---

## ⚙️ Requisitos

- Python ≥ 3.8
- `pandas`
- `openai`, `groq`, `google-generativeai`
- Claves API personales para cada proveedor

Instalación rápida:
```bash
pip install pandas openai groq google-generativeai
```

---

## 📝 Notas

- Los archivos Excel y JSONL generados no están incluidos en este repositorio por su tamaño. Puedes consultarlos y descargarlos desde el depósito en Zenodo:
  🔗 [Archivos de resultados](https://doi.org/10.5281/zenodo.15714532)

- Reemplaza las claves API en los scripts antes de ejecutar.

---

© 2025 Javier González Pérez — Proyecto de Fin de Grado (UPM)  
Licencia MIT
