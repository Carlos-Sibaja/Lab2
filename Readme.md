# Web Scraping and Text Analysis Project

## Overview
This project focuses on learning and applying web scraping techniques and text analysis using modern libraries and tools. The goal is to scrape data from a public website, analyze the collected text using sentiment analysis and summarization algorithms, and present the results in a structured format.

---

## Explanation of the Results
After analyzing 100 news articles related to Trump from **El País**, two sets of sentiment analysis results were obtained using two different libraries. A second library was used because the text was in Spanish, and feedback suggested that using translated, adapted, or foreign texts (like El País articles originally in Spanish, even if translated) might misinterpret the sentiment. This allowed me to observe how different the results could be.

### Sentiment Direction
- **Hugging Face**: The articles have an average sentiment direction of **-0.88**, suggesting that the majority of the articles express a clearly negative sentiment toward Trump.
- **NLTK**: The average sentiment direction is **0.25**, indicating that, on average, the articles tend to show a slightly positive or neutral sentiment.

### Importance Scores
- **Hugging Face**: Provides an average importance score of **0.3069**, suggesting that the model detected a moderate level of importance in the text features used to make the sentiment predictions.
- **NLTK**: Does not provide an importance score.

### Confidence Scores
- **Hugging Face**: The average confidence score is **0.3753**.
- **NLTK**: The average confidence score is **0.2385**.
Although both scores are relatively low, Hugging Face appears to be more confident in its predictions than NLTK.

### Conclusion
Based on Hugging Face's results, we can conclude that the articles analyzed tend to have a negative tone regarding Trump. However, the difference in results between the two libraries highlights the challenges of sentiment analysis on translated or adapted texts.

---

## Project Structure
The project is divided into two main parts:

### **Part 1: Web Scraping**
1. Researched and compared popular web scraping libraries, including:
   - **Scrapy**
   - **BeautifulSoup**
   - **MechanicalSoup**
   - **Playwright** (browser automation)
   - **Selenium** (used for benchmarking but removed in the final version).

2. Selected **Playwright** for its ease of use, modern browser automation capabilities, and ability to handle dynamic content.

3. Scraped a public news website (**El País**) to collect at least 100 articles on a specific topic related to "Trump."

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
   - Sentiment direction (positive or negative).
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
  - Summarization using the Sumy LSA Summarizer.
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
- **ftfy**: For cleaning text. Spanish characters created difficulties during sentiment processing.

---

## How to Run the Project
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Local URL: http://localhost:8501
   Network URL: http://10.0.0.44:8501
   https://lab2-sentiment.streamlit.app/

## Documentation
1. **GitHub** https://github.com/Carlos-Sibaja/Lab2.git