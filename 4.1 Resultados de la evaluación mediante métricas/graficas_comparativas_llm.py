# ==========================================================
#  Proyecto: IMPLEMENTACIÓN DE UN SISTEMA DE EVALUACIÓN DE CAPACIDADES DE GRANDES MODELOS DE LENGUAJE A TRAVÉS DE BUCLES DE RESUMEN Y EXTENSIÓN DE TEXTOS
#  Apartado: 4. Resultados
#            4.1 Resultados de la evaluación mediante métricas
#  Autor: Javier González Pérez
#  Fecha: 03/06/2025
#  Descripción: Script para análisis y visualización de métricas de evaluación de modelos de lenguaje a lo largo de
#  distintas iteraciones y comparaciones entre modelos. Lee métricas desde archivos Excel, transforma los datos para 
#  facilitar el análisis por iteración y tipo de métrica, y genera gráficas combinadas (líneas y barras) para precision,
#  recall y f1-score. Permite comparar el rendimiento de varios modelos (por ejemplo, GPT-4 Mini y Gemini) y guarda las
#  gráficas en un directorio específico.
# ==========================================================
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

# Configuración de estilo para las gráficas
sns.set_theme(style="whitegrid")  # Configura el estilo directamente con Seaborn
sns.set_palette("colorblind")  # Paleta de colores accesible

# Función para transformar los datos y agregar la columna 'iteration'
def transform_data_for_iterations(df, metric_prefix):
    """
    Transforma un DataFrame con columnas que contienen métricas por iteración en un formato más adecuado para análisis.

    Args:
        df (pd.DataFrame): DataFrame original con columnas que contienen métricas por iteración.
        metric_prefix (str): Prefijo que identifica las columnas relacionadas con las métricas (por ejemplo, 'summary' o 'new_text').

    Returns:
        pd.DataFrame: DataFrame transformado con las columnas: 'id', 'iteration', 'metric_type', 'value'.
    """
    iteration_data = []  # Lista para almacenar los datos transformados

    for col in df.columns:
        if col.startswith(metric_prefix):
            try:
                if metric_prefix == 'new_text':
                    iteration = int(col.split('_')[2])
                else:
                    iteration = int(col.split('_')[1])

                metric_type = col.split('-')[-1]

                for _, row in df.iterrows():
                    iteration_data.append({
                        'id': row['id'],
                        'iteration': iteration,
                        'metric_type': metric_type,
                        'value': row[col]
                    })

            except (IndexError, ValueError):
                print(f"Error procesando la columna: {col}. Verifica el formato.")

    return pd.DataFrame(iteration_data)

# Función para generar y guardar gráficas combinadas para las métricas
def plot_combined_metrics(df, model_name, sheet_name, output_dir="graficas_finales"):
    """
    Genera y guarda una gráfica combinada para las métricas precision, recall y f1.

    Args:
        df (pd.DataFrame): DataFrame con los datos transformados.
        model_name (str): Nombre del modelo (por ejemplo, 'GPT-4 Mini').
        sheet_name (str): Nombre de la pestaña del archivo Excel.
        output_dir (str): Directorio donde se guardarán las gráficas.
    """
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(12, 8))  # Aumentar el tamaño de la figura
    for metric_name in ['precision', 'recall', 'f1']:
        metric_data = df[df['metric_type'] == metric_name]
        grouped = metric_data.groupby('iteration')['value'].agg(['mean', 'std'])
        plt.errorbar(grouped.index, grouped['mean'], yerr=grouped['std'], 
                     fmt='-o', capsize=5, label=metric_name.capitalize(), 
                     linewidth=2, markersize=8)
    
    plt.title(f'Metrics Across Iterations ({model_name} - {sheet_name})', fontsize=18, fontweight='bold')
    plt.xlabel('Iteration', fontsize=16)
    plt.ylabel('Metric Value', fontsize=16)
    plt.legend(fontsize=14)
    plt.grid(alpha=0.5)
    plt.tight_layout()

    output_file = os.path.join(output_dir, f"{model_name}_{sheet_name}.png")
    plt.savefig(output_file, format='png', bbox_inches='tight', dpi=400)  # Ajustar para evitar recortes y mejorar calidad
    print(f"Gráfica guardada en: {output_file}")
    plt.close()

# Función para generar un gráfico de barras agrupadas
def plot_model_comparison_bar_chart(data, models, iterations, metric, output_dir="graficas_finales"):
    """
    Genera un gráfico de barras agrupadas para comparar modelos en iteraciones específicas.

    Args:
        data (pd.DataFrame): DataFrame con los datos transformados.
        models (list): Lista de nombres de los modelos.
        iterations (list): Lista de iteraciones a incluir (por ejemplo, [1, 5, 10]).
        metric (str): Métrica a graficar (por ejemplo, 'f1').
        output_dir (str): Directorio donde se guardará la gráfica.
    """
    os.makedirs(output_dir, exist_ok=True)

    filtered_data = data[(data['iteration'].isin(iterations)) & (data['metric_type'] == metric)]
    pivot_data = filtered_data.pivot_table(index='iteration', columns='model', values='value', aggfunc='mean')

    ax = pivot_data.plot(kind='bar', figsize=(12, 8), color=['#1f77b4', '#ff7f0e'])  # Colores personalizados
    plt.title(f'Comparación de Modelos - {metric.capitalize()}', fontsize=18, fontweight='bold')
    plt.xlabel('Iteración', fontsize=16)
    plt.ylabel(f'Valor de {metric.capitalize()}', fontsize=16)
    plt.legend(title='Modelos', fontsize=14)
    plt.grid(axis='y', alpha=0.5)

    # Añadir etiquetas de valores en las barras
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                    textcoords='offset points')

    plt.tight_layout()
    output_file = os.path.join(output_dir, f"model_comparison_{metric}.png")
    plt.savefig(output_file, format='png', bbox_inches='tight', dpi=400)  # Ajustar para evitar recortes y mejorar calidad
    print(f"Gráfica guardada en: {output_file}")
    plt.close()

# Main
if __name__ == "__main__":
    # Lista de archivos y nombres de modelos
    files = [
        ('output_gpt4-mini_1000_incremental.xlsx', 'GPT-4 Mini'),
        ('textos_gemini_stats.xlsx', 'gemini-1.5-flash')  # Añade el archivo del segundo modelo
    ]

    # Hojas y prefijos de métricas
    sheets_and_prefixes = [
        ('orig_txt-summ_ROUGE_temp1.0', 'summary'),
        ('orig_txt-txts_ROUGE_temp1.0', 'new_text'),
        ('orig_sum-summ_ROUGE_temp1.0', 'summary'),
        ('orig_txt-summ_BERT_temp1.0', 'summary'),
        ('orig_txt-txts_BERT_temp1.0', 'new_text'),
        ('orig_sum-summ_BERT_temp1.0', 'summary'),
    ]

    combined_data = []

    for file_path, model_name in files:
        if not os.path.exists(file_path):
            print(f"El archivo {file_path} no existe. Saltando...")
            continue

        for sheet_name, metric_prefix in sheets_and_prefixes:
            print(f"Procesando {sheet_name} para {model_name}...")
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                transformed_data = transform_data_for_iterations(df, metric_prefix=metric_prefix)

                if transformed_data.empty:
                    print(f"Advertencia: No se generaron datos transformados para {sheet_name}.")
                    continue

                transformed_data['model'] = model_name
                combined_data.append(transformed_data)

                plot_combined_metrics(
                    transformed_data,
                    model_name,
                    sheet_name,
                    output_dir="graficas_finales"
                )
            except Exception as e:
                print(f"Error procesando la hoja {sheet_name}: {e}")

    if combined_data:
        combined_data = pd.concat(combined_data, ignore_index=True)
        print("Datos combinados generados correctamente.")

        # Comparar modelos en iteraciones específicas
        for metric in ['f1', 'precision', 'recall']:
            plot_model_comparison_bar_chart(
                combined_data,
                models=['GPT-4 Mini', 'gemini-1.5-flash'],  # Ajusta los nombres de los modelos
                iterations=[1, 5, 10],
                metric=metric,
                output_dir="graficas_finales"
            )
    else:
        print("No se generaron datos combinados.")