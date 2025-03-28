import pandas as pd
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from transformers import pipeline, AutoTokenizer
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
import streamlit as st

# Initialize Hugging Face sentiment pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

# Initialize NLTK Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

def generate_summary(text, sentence_count=2):
    """
    Generates a summary of the given text using the LSA summarizer.

    Args:
        text (str): The input text to summarize.
        sentence_count (int): The number of sentences to include in the summary.

    Returns:
        str: The generated summary.
    """
    parser = PlaintextParser.from_string(text, Tokenizer("spanish"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)

def analyze_text_huggingface(text):
    """
    Analyzes the sentiment of the given text using Hugging Face's sentiment pipeline.

    Args:
        text (str): The input text to analyze.

    Returns:
        tuple: A tuple containing the confidence score and the sentiment direction.
    """
    result = sentiment_pipeline(text, truncation=True)
    label = result[0]["label"]
    score = result[0]["score"]

    stars = int(label.split()[0])  # Extract the number of stars
    if stars <= 2:
        direction = "negative"
    elif stars == 3:
        direction = "neutral"
    else:
        direction = "positive"

    return score, direction

def analyze_text_nltk(text):
    """
    Analyzes the sentiment of the given text using NLTK's SentimentIntensityAnalyzer.

    Args:
        text (str): The input text to analyze.

    Returns:
        tuple: A tuple containing the compound score and the sentiment direction.
    """
    sentiment_scores = sia.polarity_scores(text)
    compound_score = sentiment_scores["compound"]  # Compound score from -1 to 1

    # Determine sentiment direction
    if compound_score >= 0.05:
        direction = "positive"
    elif compound_score <= -0.05:
        direction = "negative"
    else:
        direction = "neutral"

    return compound_score, direction

def split_text_by_tokens(text, max_tokens=512):
    """
    Splits the given text into smaller chunks based on the maximum token limit.

    Args:
        text (str): The input text to split.
        max_tokens (int): The maximum number of tokens per chunk.

    Yields:
        str: A chunk of the text.
    """
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
    """
    Analyzes the sentiment of texts in a CSV file using Hugging Face and NLTK.

    Args:
        input_file (str): The path to the input CSV file.
        output_file (str): The path to the output CSV file where results will be saved.
    """
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
            # Generate summary
            summary = generate_summary(text, sentence_count=2)

            # Analyze with Hugging Face
            fragments = list(split_text_by_tokens(text))
            scores_hugging = []
            directions_hugging = []

            for fragment in fragments:
                score_hugging, direction_hugging = analyze_text_huggingface(fragment)
                scores_hugging.append(score_hugging)
                directions_hugging.append(direction_hugging)

            average_score_hugging = sum(scores_hugging) / len(scores_hugging)
            final_direction_hugging = max(set(directions_hugging), key=directions_hugging.count)

            # Analyze with NLTK
            confidence_score_nltk, direction_nltk = analyze_text_nltk(text)

            # Normalize importance score to range [-1, 1]
            importance_score = (average_score_hugging + confidence_score_nltk) / 2

            # Update DataFrame
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

    # Reorder columns
    column_order = [
        "title",
        "importance_score",
        "direction_hugging",
        "confidence_score_hugging",
        "direction_nltk",
        "confidence_score_nltk",
        "summary",  # Keep summary at the end if needed
        "text"      # Keep the original text at the end if needed
    ]
    df = df[column_order]

    # Save the reordered DataFrame to the output CSV
    df.to_csv(output_file, index=False)
    print(f"✅ Analysis complete. Output saved to '{output_file}'")

def create_summary_dataframe(df):
    """
    Creates a summary DataFrame with average sentiment direction, confidence scores, 
    and the average importance score.

    Args:
        df (DataFrame): The input DataFrame containing sentiment analysis results.

    Returns:
        DataFrame: A summary DataFrame with averages for each library and the importance score.
    """
    # Calculate average sentiment direction for Hugging Face and NLTK
    hugging_avg_direction = df["direction_hugging"].apply(lambda x: 1 if x == "positive" else -1 if x == "negative" else 0).mean()
    nltk_avg_direction = df["direction_nltk"].apply(lambda x: 1 if x == "positive" else -1 if x == "negative" else 0).mean()

    # Calculate average confidence scores
    hugging_avg_confidence = df["confidence_score_hugging"].mean()
    nltk_avg_confidence = df["confidence_score_nltk"].mean()

    # Calculate average importance score
    avg_importance_score = df["importance_score"].mean()

    # Create the summary DataFrame
    summary_df = pd.DataFrame({
        "Metric": ["Average Direction", "Average Confidence Score", "Average Importance Score"],
        "Hugging Face": [hugging_avg_direction, hugging_avg_confidence, avg_importance_score],
        "NLTK": [nltk_avg_direction, nltk_avg_confidence, None]  # Importance score is not library-specific
    })
    print(summary_df)
    return summary_df

def plot_sentiment_distribution(df):
    """
    Plots the sentiment distribution for Hugging Face and NLTK.

    Args:
        df (DataFrame): The input DataFrame containing sentiment analysis results.
    """
    # Create a smaller figure
    fig, axes = plt.subplots(1, 2, figsize=(6, 4), sharey=True)  # Smaller size (8x4)

    # Define the consistent order of sentiment categories
    sentiment_order = ["positive", "neutral", "negative"]

    # Hugging Face sentiment distribution
    hugging_counts = df["direction_hugging"].value_counts().reindex(sentiment_order, fill_value=0)
    axes[0].bar(hugging_counts.index, hugging_counts.values, color=["green", "blue", "red"])
    axes[0].set_title("Hugging Face Sentiment Distribution", fontsize=8)
    axes[0].set_xlabel("Sentiment", fontsize=8)
    axes[0].set_ylabel("Count", fontsize=8)

    # NLTK sentiment distribution
    nltk_counts = df["direction_nltk"].value_counts().reindex(sentiment_order, fill_value=0)
    axes[1].bar(nltk_counts.index, nltk_counts.values, color=["green", "blue", "red"])
    axes[1].set_title("NLTK Sentiment Distribution", fontsize=8)
    axes[1].set_xlabel("Sentiment", fontsize=8)

    # Adjust layout to center the plots and reduce whitespace
    plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.2, wspace=0.4)

    # Display the plot in Streamlit
    st.pyplot(fig)

if __name__ == "__main__":
    input_file = "trump100_elpais_with_text.csv"
    output_file = "trump_analyzed.csv"

    analyze_csv(input_file, output_file)
    df = pd.read_csv(output_file)
    summary_df = create_summary_dataframe(df)
    print(summary_df)
    plot_sentiment_distribution(df)




