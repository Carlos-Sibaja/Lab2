# Web Scraping and Text Analysis Project

## Overview
This project focuses on learning and applying web scraping techniques and text analysis using modern libraries and tools. The goal is to scrape data from a public website, analyze the collected text using sentiment analysis and summarization algorithms, and present the results in a structured format.

---

## Project Structure
The project is divided into two main parts:

### **Part 1: Web Scraping**
1. Researched and compared popular web scraping libraries, including:
   - **Scrapy**
   - **BeautifulSoup**
   - **MechanicalSoup**
   - **Playwright** (browser automation)
2. Selected **Playwright** for its ease of use, modern browser automation capabilities, and ability to handle dynamic content.
3. Scraped a public news website (**El País**) to collect at least 100 articles on a specific topic (e.g., "Trump").
4. Extracted the main content of each article by targeting `<p>` tags within the article body.
5. Saved the scraped data (titles, URLs, and article texts) into a CSV file (`trump100_elpais_with_text.csv`).

### **Part 2: Text Analysis**
1. Applied **sentiment analysis** using two libraries:
   - **Hugging Face Transformers**: For multilingual sentiment analysis.
   - **NLTK SentimentIntensityAnalyzer**: For polarity scoring.
2. Generated a **summary** for each article using the **Sumy LSA Summarizer**.
3. Calculated an **importance score** for each article based on:
   - Sentiment confidence scores.
   - Text length.
   - Direction (positive or negative).
4. Presented the results in a tabulated format (`trump_analyzed.csv`) with the following columns:
   - `title`: Title of the article.
   - `importance_score`: A normalized score between `-1` and `1` indicating the importance of the article.
   - `direction_hugging`: Sentiment direction (positive, neutral, or negative) from Hugging Face.
   - `confidence_score_hugging`: Confidence score from Hugging Face.
   - `direction_nltk`: Sentiment direction from NLTK.
   - `confidence_score_nltk`: Confidence score from NLTK.
   - `summary`: A brief summary of the article.
   - `text`: The full text of the article.

---

## Internal Structure
The project is organized into the following files:

### **1. `a_scraper.py`**
- Handles web scraping using Playwright.
- Collects article metadata (titles and URLs) and saves it to `trump100_elpais.csv`.

### **2. `b_extract_text.py`**
- Extracts the main content of each article by visiting the URLs collected in `a_scraper.py`.
- Cleans and concatenates the text from `<p>` tags.
- Saves the extracted text to `trump100_elpais_with_text.csv`.

### **3. `c_LLM.py`**
- Performs text analysis, including:
  - Sentiment analysis using Hugging Face and NLTK.
  - Summarization using Sumy LSA Summarizer.
  - Calculation of the importance score.
- Saves the analyzed data to `trump_analyzed.csv`.
- Generates a summary DataFrame with average metrics and visualizes sentiment distributions.

### **4. `d_elpais.py`**
- The main script that coordinates the entire workflow:
  1. Scrapes metadata.
  2. Extracts article texts.
  3. Performs text analysis.
  4. Generates a summary and visualizations.

---

## Tools and Libraries Used
- **Playwright**: For web scraping and browser automation.
- **Pandas**: For data manipulation and CSV handling.
- **Hugging Face Transformers**: For multilingual sentiment analysis.
- **NLTK**: For polarity-based sentiment analysis.
- **Sumy**: For text summarization using the LSA algorithm.
- **Matplotlib**: For visualizing sentiment distributions.
- **Streamlit**: For displaying plots interactively.

---

## How to Run the Project
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt