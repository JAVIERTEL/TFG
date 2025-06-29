# ==========================================================
#  Proyecto: IMPLEMENTACIÓN DE UN SISTEMA DE EVALUACIÓN DE CAPACIDADES DE GRANDES MODELOS DE LENGUAJE A TRAVÉS DE BUCLES DE RESUMEN Y EXTENSIÓN DE TEXTOS
#  Apartado: 4. Resultados
#            4.2 Resultados de la retención semántica a través de test automatizados
#  Autor: Javier González Pérez
#  Fecha: 03/06/2025
#  Descripción: Script para comparar respuestas generadas por ChatGPT-4 con las respuestas correctas de referencia. 
#  Lee ambos archivos Excel, cruza cada respuesta con la opción correcta correspondiente, y determina si la respuesta 
#  es correcta, incorrecta o si hay algún error de correspondencia. El resultado se guarda en un nuevo archivo Excel
#  con el detalle de la comparación para cada pregunta.
# ==========================================================

import pandas as pd

# Archivos de entrada
file_respuestas = "respuestas_gpt4_excel.xlsx"
file_correctas = "preguntas_gpt4.xlsx"

# Leer ambos archivos
df_respuestas = pd.read_excel(file_respuestas)
df_correctas = pd.read_excel(file_correctas)

# Crear una lista para almacenar los resultados
resultados = []

# Iterar sobre las filas del archivo de respuestas
for index, row in df_respuestas.iterrows():
    id_texto = row["id"]
    pregunta = row["pregunta"]
    respuesta = row["respuesta"]
    tipo_texto = row["tipo_texto"]  # Obtener el valor de la columna tipo_texto

    # Validar que la pregunta esté dentro del rango Q1 a Q10
    if pregunta.startswith("Q") and pregunta[1:].isdigit() and 1 <= int(pregunta[1:]) <= 10:
        # Buscar la fila correspondiente en el archivo de respuestas correctas
        fila_correcta = df_correctas[df_correctas["id"] == id_texto]

        if not fila_correcta.empty:
            # Extraer la respuesta correcta para la pregunta específica
            columna_correcta = f"Correct_Option_{pregunta[1:]}"  # Extraer el número de la pregunta (Q1 -> 1)
            respuesta_correcta = fila_correcta.iloc[0][columna_correcta]

            # Asegurarse de que ambos valores sean cadenas y no nulos
            if isinstance(respuesta, float) or pd.isna(respuesta):
                respuesta = ""
            if isinstance(respuesta_correcta, float) or pd.isna(respuesta_correcta):
                respuesta_correcta = ""

            # Comparar solo la primera letra de las respuestas
            if respuesta.strip()[0:1] == respuesta_correcta.strip()[0:1]:  # [0:1] evita errores si la cadena está vacía
                resultado = "Correcta"
            else:
                resultado = "Incorrecta"
        else:
            resultado = "No encontrada en archivo de respuestas correctas"
    else:
        resultado = "Pregunta fuera de rango"

    # Agregar el resultado a la lista
    resultados.append({
        "id": id_texto,
        "pregunta": pregunta,
        "respuesta": respuesta,
        "tipo_texto": tipo_texto,  # Incluir tipo_texto en los resultados
        "resultado": resultado
    })

# Crear un DataFrame con los resultados
df_resultados = pd.DataFrame(resultados)

# Guardar el DataFrame en un nuevo archivo Excel
output_file = "resultados_gpt4.xlsx"
df_resultados.to_excel(output_file, index=False)

print(f"Archivo de comparación generado: {output_file}")
