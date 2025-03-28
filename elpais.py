# deactivate to deactivate the virtual environment  .venv\Scripts\deactivate
# .venv\Scripts\Activate.ps1 to activate the virtual environment
# python -m venv .venv to create the virtual environment
# pip install -r requirements.txt to install the required packages
# pip freeze > requirements.txt to save the installed packages
# pip install scraper
# pip python main.py
# https://www.cnn.com/2025/03/27/Tv/video/sitroom-blitzer-rounds-signal-trump-leak
# ¿Quieres que agregue el nombre del subreddit o la fecha del post también? Puedo añadirlo en un segundo.

# elpais.py

import asyncio
import pandas as pd
from urllib.parse import quote
from playwright.async_api import async_playwright
import os
from extract_text import extract_all_texts  # Importa la función correctamente
from LLM import analyze_csv  # Importa la función correctamente

SEARCH_TERMS = [
    "signal trump",
    "trump Guerra comercial",
    "trump Elon Musk",
    "trump aranceles",
    "trump presidente",
    "trump Deportaciones",
    "trump noticias",
    "trump economía",
    "trump Derechos LGBTQ",
    "trump inmigración",
]

async def scrape_elpais():
    base_url = "https://elpais.com/buscador/?q="
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for term in SEARCH_TERMS:
            query_url = base_url + quote(term)
            print(f"🔍 Searching: {query_url}")
            await page.goto(query_url)
            await page.wait_for_timeout(3000)

            articles = await page.query_selector_all("article")
            print(f"📄 Found {len(articles)} articles for '{term}'")

            for article in articles:
                title_element = await article.query_selector("h2 a")
                if not title_element:
                    continue
                title = await title_element.inner_text()
                link = await title_element.get_attribute("href")
                date_element = await article.query_selector("time")
                date = await date_element.get_attribute("datetime") if date_element else "NO DATE"

                results.append({
                    'title': title.strip(),
                    'url': f"https://elpais.com{link}" if link.startswith("/") else link,
                    'date': date.strip() if date else 'NO DATE'
                })

                if len(results) >= 2:
                    break
            if len(results) >= 2:
                break

        await browser.close()
    return results

async def main():
    try:
        # Step 1: Scrape metadata
        elpais_results = await scrape_elpais()
        meta_df = pd.DataFrame(elpais_results)
        meta_df.to_csv("trump100_elpais.csv", index=False)
        print(f"✅ Metadata saved with {len(elpais_results)} articles")

        # Step 2: Extract article bodies
        if not elpais_results:
            print("❌ No articles found. Skipping text extraction.")
            return

        await extract_all_texts("trump100_elpais.csv", "trump100_elpais_with_text.csv")
        print("✅ Article texts extracted and saved.")

        # Step 3: Analyze content
        if not os.path.exists("trump100_elpais_with_text.csv"):
            print("❌ 'trump100_elpais_with_text.csv' not found. Skipping analysis.")
            return

        analyze_csv("trump100_elpais_with_text.csv", "analyzed_text.csv")
        print("✅ Analysis completed and saved to 'analyzed_text.csv'.")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

# Run all steps
asyncio.run(main())