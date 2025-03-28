import pandas as pd
from textblob import TextBlob
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from nltk.corpus import stopwords
import nltk
import os

#LLM.py


def generate_summary(text, sentence_count=2):
    parser = PlaintextParser.from_string(text, Tokenizer("spanish"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)

def analyze_text(text):
    summary = generate_summary(text)
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    importance = min(1.0, max(0.1, len(text) / 500))
    direction = "positive" if polarity > 0 else "negative" if polarity < 0 else "neutral"
    return summary, round(importance, 2), direction

def analyze_csv(input_file="trump100_elpais_with_text.csv", output_file="analyzed_text.csv"):
    # Leer el archivo CSV de entrada
    df = pd.read_csv(input_file)
    
    # Agregar columnas necesarias
    df["summary"] = ""
    df["importance_score"] = 0.0
    df["direction"] = ""

    # Procesar cada fila
    for i, row in df.iterrows():
        text = row.get("text", "")
        if isinstance(text, str) and text.strip():
            summary, score, direction = analyze_text(text)
        else:
            summary, score, direction = "(No content)", 0.0, "neutral"

        # Actualizar las columnas con los resultados
        df.at[i, "summary"] = summary
        df.at[i, "importance_score"] = score
        df.at[i, "direction"] = direction

    # Reorganizar las columnas en el orden deseado
    df = df.reset_index()  # Agregar un índice numérico
    df.rename(columns={"index": "id"}, inplace=True)  # Renombrar la columna del índice a "id"
    df = df[["id", "direction", "importance_score", "summary", "text", "url"]]  # Ordenar las columnas

    # Guardar el archivo CSV con los datos procesados
    df.to_csv(output_file, index=False)
    print(f"✅ Analysis complete. Output saved to '{output_file}'")
