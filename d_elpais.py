# deactivate to deactivate the virtual environment  .venv\Scripts\deactivate
# .venv\Scripts\Activate.ps1 to activate the virtual environment
# python -m venv .venv to create the virtual environment
# pip install -r requirements.txt to install the required packages
# pip freeze > requirements.txt to save the installed packages
# pip install scraper
# pip python d_elpais.py
#pip install streamlit


# d_elpais.py - Only for generating CSVs

import asyncio
import pandas as pd
import os
from a_scraper import scrape_elpais
from b_extract_text import extract_all_texts
from c_LLM import analyze_csv

async def main():
    # Step 1 - Scraping
    elpais_results = await scrape_elpais()
    meta_df = pd.DataFrame(elpais_results)
    meta_df.to_csv("trump100_elpais.csv", index=False)

    # Step 2 - Extract Texts
    await extract_all_texts("trump100_elpais.csv", "trump100_elpais_with_text.csv")

    # Step 3 - Analyze
    analyze_csv("trump100_elpais_with_text.csv", "trump_analyzed.csv")

     # ✅ Console Summary Output (ONLY when generating the CSVs)
    df = pd.read_csv("trump_analyzed.csv")
    summary_df = create_summary_dataframe(df)
    print("\nQuick Summary of the Sentiment Analysis:")
    print(summary_df)

    print("✅ Process completed successfully")

   

if __name__ == "__main__":
    asyncio.run(main())

    