# ==========================================================
#  Proyecto: IMPLEMENTACIÓN DE UN SISTEMA DE EVALUACIÓN DE CAPACIDADES DE GRANDES MODELOS DE LENGUAJE A TRAVÉS DE BUCLES DE RESUMEN Y EXTENSIÓN DE TEXTOS
#  Apartado: 4. Resultados
#            4.2 Resultados de la retención semántica a través de test automatizados
#  Autor: Javier González Pérez
#  Fecha: 03/06/2025
#  Descripción: Script para analizar y visualizar la efectividad de respuestas de Gemini según el tipo de texto evaluado.
#  Lee los resultados desde un archivo Excel, calcula el porcentaje de respuestas correctas por cada tipo de texto, y genera
#  una gráfica de barras ordenada que muestra la efectividad alcanzada en cada categoría. La gráfica se guarda en alta 
#  calidad para su uso en informes o presentaciones.
# ==========================================================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configurar estilo visual
sns.set_theme(style="whitegrid")
sns.set_palette("colorblind")

# Leer el archivo de resultados de Gemini
file_resultados = "resultados_gemini.xlsx"
df_resultados = pd.read_excel(file_resultados)

# Calcular la efectividad por tipo de texto
efectividad = df_resultados.groupby("tipo_texto").apply(
    lambda x: (x["resultado"] == "Correcta").sum() / len(x) * 100
).reset_index(name="Porcentaje de Efectividad")

# Ordenar los tipos de texto por efectividad descendente para mejor visualización
efectividad = efectividad.sort_values("Porcentaje de Efectividad", ascending=False)

# Crear carpeta para guardar gráficas
os.makedirs("graficas_finales", exist_ok=True)

# Crear la gráfica
plt.figure(figsize=(12, 8))
ax = sns.barplot(
    data=efectividad,
    x="tipo_texto",
    y="Porcentaje de Efectividad",
    edgecolor="black"
)

# Añadir etiquetas con los valores encima de cada barra
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{height:.1f}%', (p.get_x() + p.get_width() / 2., height),
                ha='center', va='bottom', fontsize=11, color='black', xytext=(0, 5),
                textcoords='offset points')

# Títulos y etiquetas
plt.title("Efectividad por Tipo de Texto (Gemini)", fontsize=18, fontweight='bold')
plt.xlabel("Tipo de Texto", fontsize=14)
plt.ylabel("Porcentaje de Efectividad (%)", fontsize=14)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Guardar la gráfica en alta calidad
plt.savefig("efectividad_gemini_por_tipo_texto.png", dpi=400, bbox_inches='tight')
plt.show()
