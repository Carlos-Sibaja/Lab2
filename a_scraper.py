import asyncio
import pandas as pd
from urllib.parse import quote
from playwright.async_api import async_playwright
from b_extract_text import extract_all_texts  
from c_LLM import analyze_csv, create_summary_dataframe, plot_sentiment_distribution

# a_scraper.py

# Define the search terms
SEARCH_TERMS = [
    "trump",
    "trump logros",
    "signal",
    "trump aranceles",
    "ucrania",
    "trump deportaciones",
    "MAGA",
    "trump avance económico",
    "acuerdo de paz",
    "inmigración",
    "trump inmigración",
]

# Function to scrape articles from El País
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

                results.append({
                    'title': title.strip(),
                    'url': f"https://elpais.com{link}" if link.startswith("/") else link
                })

                if len(results) >= 10:
                    break
            if len(results) >= 10:
                break

        await browser.close()
    return results

if __name__ == "__main__":
    asyncio.run(scrape_elpais())
