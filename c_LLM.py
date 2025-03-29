# c_LLM.py

import pandas as pd
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from transformers import pipeline, AutoTokenizer
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
import streamlit as st
import nltk
nltk.download('vader_lexicon', quiet=True)

# Initialize Hugging Face sentiment pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

# Initialize NLTK Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

def generate_summary(text, sentence_count=2):
    parser = PlaintextParser.from_string(text, Tokenizer("spanish"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)

def analyze_text_huggingface(text):
    result = sentiment_pipeline(text, truncation=True)
    label = result[0]["label"]
    score = result[0]["score"]

    stars = int(label.split()[0])
    if stars <= 2:
        direction = "negative"
    elif stars == 3:
        direction = "neutral"
    else:
        direction = "positive"

    return score, direction

def analyze_text_nltk(text):
    sentiment_scores = sia.polarity_scores(text)
    compound_score = sentiment_scores["compound"]

    if compound_score >= 0.05:
        direction = "positive"
    elif compound_score <= -0.05:
        direction = "negative"
    else:
        direction = "neutral"

    return compound_score, direction

def split_text_by_tokens(text, max_tokens=512):
    words = text.split()
    current_chunk = []
    current_len = 0

    for word in words:
        token_len = len(tokenizer.tokenize(word))
        if current_len + token_len > max_tokens:
            yield " ".join(current_chunk)
            current_chunk = []
            current_len = 0
        current_chunk.append(word)
        current_len += token_len

    if current_chunk:
        yield " ".join(current_chunk)

def analyze_csv(input_file="trump100_elpais_with_text.csv", output_file="trump_analyzed.csv"):
    df = pd.read_csv(input_file)
    df["summary"] = ""
    df["importance_score"] = 0.0
    df["direction_hugging"] = ""
    df["confidence_score_hugging"] = 0.0
    df["direction_nltk"] = ""
    df["confidence_score_nltk"] = 0.0

    for i, row in df.iterrows():
        text = row.get("text", "")
        if isinstance(text, str) and text.strip():
            summary = generate_summary(text, sentence_count=2)

            fragments = list(split_text_by_tokens(text))
            scores_hugging = []
            directions_hugging = []

            for fragment in fragments:
                score_hugging, direction_hugging = analyze_text_huggingface(fragment)
                scores_hugging.append(score_hugging)
                directions_hugging.append(direction_hugging)

            average_score_hugging = sum(scores_hugging) / len(scores_hugging)
            final_direction_hugging = max(set(directions_hugging), key=directions_hugging.count)

            confidence_score_nltk, direction_nltk = analyze_text_nltk(text)

            importance_score = (average_score_hugging + confidence_score_nltk) / 2

            df.at[i, "summary"] = summary
            df.at[i, "importance_score"] = importance_score
            df.at[i, "confidence_score_hugging"] = average_score_hugging
            df.at[i, "direction_hugging"] = final_direction_hugging
            df.at[i, "confidence_score_nltk"] = confidence_score_nltk
            df.at[i, "direction_nltk"] = direction_nltk
        else:
            df.at[i, "summary"] = ""
            df.at[i, "importance_score"] = 0.0
            df.at[i, "confidence_score_hugging"] = 0.0
            df.at[i, "direction_hugging"] = "neutral"
            df.at[i, "confidence_score_nltk"] = 0.0
            df.at[i, "direction_nltk"] = "neutral"

    column_order = [
        "title",
        "importance_score",
        "direction_hugging",
        "confidence_score_hugging",
        "direction_nltk",
        "confidence_score_nltk",
        "summary",
        "text"
    ]
    df = df[column_order]

    df.to_csv(output_file, index=False)
    print(f"✅ Analysis complete. Output saved to '{output_file}'")

def create_summary_dataframe(df):
    hugging_avg_direction = df["direction_hugging"].apply(lambda x: 1 if x == "positive" else -1 if x == "negative" else 0).mean()
    nltk_avg_direction = df["direction_nltk"].apply(lambda x: 1 if x == "positive" else -1 if x == "negative" else 0).mean()

    hugging_avg_confidence = df["confidence_score_hugging"].mean()
    nltk_avg_confidence = df["confidence_score_nltk"].mean()

    avg_importance_score = df["importance_score"].mean()

    summary_df = pd.DataFrame({
        "Metric": ["Average Direction", "Average Confidence Score", "Average Importance Score"],
        "Hugging Face": [hugging_avg_direction, hugging_avg_confidence, avg_importance_score],
        "NLTK": [nltk_avg_direction, nltk_avg_confidence, None]
    })
    print(summary_df)
    return summary_df

def plot_sentiment_distribution(df):
    fig, axes = plt.subplots(1, 2, figsize=(8, 4), sharey=True)
    sentiment_order = ["positive", "neutral", "negative"]

    hugging_counts = df["direction_hugging"].value_counts().reindex(sentiment_order, fill_value=0)
    axes[0].bar(hugging_counts.index, hugging_counts.values, color=["green", "blue", "red"])
    axes[0].set_title("Hugging Face Sentiment Distribution", fontsize=8)
    axes[0].set_xlabel("Sentiment", fontsize=8)
    axes[0].set_ylabel("Count", fontsize=6)

    nltk_counts = df["direction_nltk"].value_counts().reindex(sentiment_order, fill_value=0)
    axes[1].bar(nltk_counts.index, nltk_counts.values, color=["green", "blue", "red"])
    axes[1].set_title("NLTK Sentiment Distribution", fontsize=8)
    axes[1].set_xlabel("Sentiment", fontsize=8)

    plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.2, wspace=0.4)

    st.markdown("""
        <div style="display: flex; justify-content: center; margin-top: 20px;">
            <div style="width:33%; border: 1px solid #ddd; padding: 10px; border-radius: 10px;">
    """, unsafe_allow_html=True)
    st.pyplot(fig, use_container_width=True)
    st.markdown("""
            </div>
        </div>
    """, unsafe_allow_html=True)





