# Run the Streamlit app:
#   streamlit run a_app.py
#   streamlit run a_app.py --server.port 8501 (to run on a different port)
# Hosted App Example: https://stockprice-lab1.streamlit.app/

import streamlit as st
import pandas as pd
import os
from c_LLM import plot_sentiment_distribution, create_summary_dataframe

# Streamlit Page Configuration
st.set_page_config(
    page_title="Trump Sentiment",
    page_icon="🧐",
    layout="wide"
)

# --- Ajuste de ancho y centrado ---
st.markdown("""
    <style>
        .main {
            max-width: 90%;
            margin-left: 10%;
            margin-right: 10%;
        }
    </style>
""", unsafe_allow_html=True)

# Header Section
# Create two columns for the header
col1, col2 = st.columns(2)
col1.image("logo.jpg", width=200)  # Add your logo here
col2.markdown("<h1 style='color: blue; font-size: 25pt;'>CSIS 4260 – Spl. Topics in Data Analytics</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: blue; font-size: 10pt;'>Carlos Sibaja Jimenez Id: 300384848</h3>", unsafe_allow_html=True)

# Title of the application
st.markdown("<h2 style='color: orange; font-weight: bold;'>Sentiment Analysis - Trump from Newspaper El País</h2>", unsafe_allow_html=True)

# Required CSV files
csv_meta = "trump100_elpais.csv"  # Metadata file
csv_texts = "trump100_elpais_with_text.csv"  # Extracted texts file
csv_analyzed = "trump_analyzed.csv"  # Final analyzed file

# Check if all required files exist
if not (os.path.exists(csv_meta) and os.path.exists(csv_texts) and os.path.exists(csv_analyzed)):
    st.error("❌ Required CSV files not found. Please run: python elpais.py")
    st.stop()  # Stop the app if files are missing

# Step 1 - Sentiment Distribution Graph
st.header("1️⃣ Sentiment Distribution")
st.write("This graph shows the sentiment distribution of the analyzed articles.")
df_analyzed = pd.read_csv(csv_analyzed)  # Load the analyzed data
plot_sentiment_distribution(df_analyzed)  # Plot the sentiment distribution

# Step 2 - Sentiment Summary
st.header("2️⃣ Sentiment Summary")
st.write("This table summarizes the average sentiment direction, important score and confidence scores for each library.")
summary_df = create_summary_dataframe(df_analyzed)  # Create a summary DataFrame
st.dataframe(summary_df)  # Display the summary as a table

# Step 3 - Metadata CSV
st.header("3️⃣ Metadata CSV - trump100_elpais.csv")
st.write("This table shows the metadata of the articles scraped from El País.")
df_meta = pd.read_csv(csv_meta)  # Load the metadata file
st.dataframe(df_meta)  # Display the metadata as a table

# Step 4 - Extracted Texts
st.header("4️⃣ Extracted Texts - First 5 Rows")
st.write("Sample of extracted texts from the articles.")
df_texts = pd.read_csv(csv_texts)  # Load the extracted texts file
st.dataframe(df_texts.head())  # Display the first 5 rows of the extracted texts

# Step 5 - Full Analyzed CSV
st.header("5️⃣ Full Analyzed CSV")
st.write("Full analyzed data with sentiment scores and directions.")
st.dataframe(df_analyzed)  # Display the full analyzed data