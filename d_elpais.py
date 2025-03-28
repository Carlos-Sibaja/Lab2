# deactivate to deactivate the virtual environment  .venv\Scripts\deactivate
# .venv\Scripts\Activate.ps1 to activate the virtual environment
# python -m venv .venv to create the virtual environment
# pip install -r requirements.txt to install the required packages
# pip freeze > requirements.txt to save the installed packages
# pip install scraper
# pip python d_elpais.py
#pip install streamlit


# elpais.py 

# elpais.py - Solo para generar los CSVs
import asyncio
import pandas as pd
import os
from a_scraper import scrape_elpais
from b_extract_text import extract_all_texts
from c_LLM import analyze_csv

async def main():
    # Paso 1
    elpais_results = await scrape_elpais()
    meta_df = pd.DataFrame(elpais_results)
    meta_df.to_csv("trump100_elpais.csv", index=False)

    # Paso 2
    await extract_all_texts("trump100_elpais.csv", "trump100_elpais_with_text.csv")

    # Paso 3
    analyze_csv("trump100_elpais_with_text.csv", "trump_analyzed.csv")

    print("✅ Proceso completo finalizado")

if __name__ == "__main__":
    asyncio.run(main())
    