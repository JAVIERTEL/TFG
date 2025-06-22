# ==========================================================
#  Proyecto: IMPLEMENTACIÓN DE UN SISTEMA DE EVALUACIÓN DE CAPACIDADES DE GRANDES MODELOS DE LENGUAJE A TRAVÉS DE BUCLES DE RESUMEN Y EXTENSIÓN DE TEXTOS
#  Apartado: 3. DESARROLLO DEL SISTEMA EXPERIMENTAL
#            3.2 EVALUACIÓN DE MÉTRICAS
#  Autor: Javier González Pérez
#  Fecha: 03/05/2025
#  Descripción: Este script calcula métricas automáticas (ROUGE-1, BERTScore) entre textos originales, resúmenes y textos expandidos
#               leídos desde un archivo Excel, y guarda los resultados en otro archivo Excel, permitiendo el análisis comparativo de las salidas generadas.
#
#  Notas: La parte de tfidf en este proyecto fue descartada en este proyecto, pero se ha dejado el código para su posible uso futuro.
# ==========================================================

import pandas as pd
from rouge_score import rouge_scorer
import bert_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Función para calcular las métricas con Rouge-1
def calculate_rouge(reference, hypothesis):
    scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)
    scores = scorer.score(reference, hypothesis)
    return {"precision": scores['rouge1'].precision, "recall": scores['rouge1'].recall, "f1": scores['rouge1'].fmeasure}

# Función para calcular las métricas con BertScore
def calculate_bertscore(reference, hypothesis):
    P, R, F1 = bert_score.score([hypothesis], [reference], lang="en", verbose=True)
    return {"precision": P.mean().item(), "recall": R.mean().item(), "f1": F1.mean().item()}

# Función para calcular la similitud de coseno usando TF-IDF
def calculate_tfidf_similarity(reference, hypothesis):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([reference, hypothesis])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]

# Función para procesar las comparaciones
def process_comparisons(df, reference_col, comparison_cols, metric_func):
    results = []
    for index, row in df.iterrows():
        result = {"id": row["id"]}
        reference = row[reference_col]
        for col in comparison_cols:
            if pd.notna(row[col]):
                hypothesis = row[col]
                scores = metric_func(reference, hypothesis)
                result.update({f"{col}-precision": scores["precision"],
                               f"{col}-recall": scores["recall"],
                               f"{col}-f1": scores["f1"]})
        results.append(result)
    return pd.DataFrame(results)

# Función para procesar las comparaciones de TF-IDF
def process_tfidf_comparisons(df, reference_col, comparison_cols):
    results = []
    for index, row in df.iterrows():
        result = {"id": row["id"]}
        reference = row[reference_col]
        for col in comparison_cols:
            if pd.notna(row[col]):
                hypothesis = row[col]
                similarity = calculate_tfidf_similarity(reference, hypothesis)
                result[f"{col}-tfidf_similarity"] = similarity
        results.append(result)
    return pd.DataFrame(results)

def main():
    # Leer el archivo Excel original
    input_file = 'textos_gemini.xlsx'
    output_file = 'textos_gemini_stats.xlsx'

    # Leer el archivo original
    df = pd.read_excel(input_file)

    # Verificar si ya existe un archivo de salida
    if os.path.exists(output_file):
        # Leer el archivo existente
        with pd.ExcelFile(output_file) as reader:
            processed_ids = set()
            for sheet_name in reader.sheet_names:
                sheet_df = pd.read_excel(reader, sheet_name=sheet_name)
                processed_ids.update(sheet_df['id'].unique())
    else:
        processed_ids = set()

    # Filtrar las filas que ya se procesaron
    df_to_process = df[~df['id'].isin(processed_ids)]

    # Definir las columnas de referencia y comparación
    original_text_cols = [col for col in df.columns if col.startswith('new_text_')]
    original_summary_cols = [col for col in df.columns if col.startswith('summary_')]

    # Procesar comparaciones para ROUGE
    rouge_results_a = process_comparisons(df_to_process, 'original_text', original_summary_cols, calculate_rouge)
    rouge_results_b = process_comparisons(df_to_process, 'original_text', original_text_cols, calculate_rouge)
    rouge_results_c = process_comparisons(df_to_process, 'original_summary', original_summary_cols, calculate_rouge)

    # Procesar comparaciones para BERTScore
    bert_results_a = process_comparisons(df_to_process, 'original_text', original_summary_cols, calculate_bertscore)
    bert_results_b = process_comparisons(df_to_process, 'original_text', original_text_cols, calculate_bertscore)
    bert_results_c = process_comparisons(df_to_process, 'original_summary', original_summary_cols, calculate_bertscore)

    # Procesar comparaciones para TF-IDF
    tfidf_results = process_tfidf_comparisons(df_to_process, 'original_text', original_summary_cols + original_text_cols)

    # Guardar los resultados en el archivo Excel de salida
    with pd.ExcelWriter(output_file, mode='a' if os.path.exists(output_file) else 'w') as writer:
        rouge_results_a.to_excel(writer, sheet_name='orig_txt-summ_ROUGE_temp1.0', index=False)
        rouge_results_b.to_excel(writer, sheet_name='orig_txt-txts_ROUGE_temp1.0', index=False)
        rouge_results_c.to_excel(writer, sheet_name='orig_sum-summ_ROUGE_temp1.0', index=False)
        bert_results_a.to_excel(writer, sheet_name='orig_txt-summ_BERT_temp1.0', index=False)
        bert_results_b.to_excel(writer, sheet_name='orig_txt-txts_BERT_temp1.0', index=False)
        bert_results_c.to_excel(writer, sheet_name='orig_sum-summ_BERT_temp1.0', index=False)
        tfidf_results.to_excel(writer, sheet_name='orig_txt-summ_TFIDF_temp1.0', index=False)

if __name__ == "__main__":
    main()
