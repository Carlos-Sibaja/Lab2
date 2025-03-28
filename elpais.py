# deactivate to deactivate the virtual environment  .venv\Scripts\deactivate
# .venv\Scripts\Activate.ps1 to activate the virtual environment
# python -m venv .venv to create the virtual environment
# pip install -r requirements.txt to install the required packages
# pip freeze > requirements.txt to save the installed packages
# pip install scraper
# pip python main.py
# https://www.cnn.com/2025/03/27/Tv/video/sitroom-blitzer-rounds-signal-trump-leak

import asyncio
import pandas as pd
import os
from a_scraper import scrape_elpais  # Importa la función de scraping desde a_scraper.py
from b_extract_text import extract_all_texts  # Importa la función para extraer texto
from c_LLM import analyze_csv, create_summary_dataframe, plot_sentiment_distribution

async def main():
    try:
        # Step 1: Scrape metadata
        print("🔍 Starting scraping...")
        elpais_results = await scrape_elpais()  # Llama a la función scrape_elpais desde a_scraper.py
        meta_df = pd.DataFrame(elpais_results)
        meta_df.to_csv("trump100_elpais.csv", index=False)
        print(f"✅ Metadata saved with {len(elpais_results)} articles")

        # Step 2: Extract article bodies
        if not elpais_results:
            print("❌ No articles found. Skipping text extraction.")
            return

        print("📝 Extracting article texts...")
        await extract_all_texts("trump100_elpais.csv", "trump100_elpais_with_text.csv")
        print("✅ Article texts extracted and saved.")

        # Step 3: Analyze content
        input_file = "trump100_elpais_with_text.csv"
        output_file = "trump_analyzed.csv"

        if not os.path.exists(input_file):
            print(f"❌ '{input_file}' not found. Skipping analysis.")
            return

        print("📊 Running sentiment analysis...")
        analyze_csv(input_file, output_file)
        print("✅ Analysis completed and saved to 'trump_analyzed.csv'.")

        # Step 4: Load analyzed data
        df = pd.read_csv(output_file)

        # Step 5: Create a summary DataFrame for benchmarking
        print("📈 Creating summary DataFrame...")
        summary_df = create_summary_dataframe(df)
        print("\nSummary of Sentiment Analysis:")
        print(summary_df)

        # Step 6: Visualize sentiment distribution
        print("📊 Plotting sentiment distribution...")
        plot_sentiment_distribution(df)

        print("🎉 All steps completed successfully!")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

# Run all steps
if __name__ == "__main__":
    asyncio.run(main())