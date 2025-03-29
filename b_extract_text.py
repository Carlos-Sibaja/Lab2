# b_extract_text.py

import asyncio
import pandas as pd
from playwright.async_api import async_playwright
from ftfy import fix_text

INPUT_CSV = "trump100_elpais.csv"
OUTPUT_CSV = "trump100_elpais_with_text.csv"

# Extract cleaned text from a single article URL
async def extract_text(page, url):
    try:
        await page.goto(url, timeout=30000)
        await page.wait_for_selector("div.a_c.clearfix[data-dtm-region='articulo_cuerpo'] p", timeout=5000)
        paragraphs = await page.query_selector_all("div.a_c.clearfix[data-dtm-region='articulo_cuerpo'] p")
        text_lines = []

        for p in paragraphs:
            raw_text = await p.inner_text()
            text = fix_text(raw_text)
            text_lower = text.lower()

            if any(keyword in text_lower for keyword in [
                "twitter", "facebook", "linkedin", "subscribe", "comments",
                "share", "author", "signature", "newsletter", "instagram",
                "see biography", "more information", "sponsored content",
                "about the author", "receive our newsletter", "latest news",
                "most viewed", "go to comments", "comments closed",
                "keep reading", "already a subscriber"
            ]):
                continue

            if len(text.strip()) < 30:
                continue

            text_lines.append(text.strip())

        full_text = "\n".join(text_lines).strip()
        words = full_text.split()
        if len(words) > 500:
            full_text = " ".join(words[:500]) + "..."

        return full_text

    except Exception as e:
        print(f"❌ Failed to extract from {url}: {e}")
        return ""

# Loop through all articles and extract texts
async def extract_all_texts(input_csv, output_csv):
    try:
        df = pd.read_csv(input_csv, encoding="utf-8")
        df["text"] = ""

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            for i, row in df.iterrows():
                url = row["link"] if "link" in row else row["url"]
                print(f"🔍 Extracting post #{i+1}: {url}")
                text = await extract_text(page, url)
                df.at[i, "text"] = text

            await browser.close()

        if "date" in df.columns:
            df = df.drop(columns=["date"])

        df.to_csv(output_csv, index=False, encoding="utf-8")
        print(f"\n✅ Saved cleaned text to {output_csv}")

    except Exception as e:
        print(f"❌ An error occurred during text extraction: {e}")

if __name__ == "__main__":
    asyncio.run(extract_all_texts(INPUT_CSV, OUTPUT_CSV))


