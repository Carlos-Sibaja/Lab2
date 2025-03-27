# deactivate to deactivate the virtual environment  .venv\Scripts\deactivate
# .venv\Scripts\Activate.ps1 to activate the virtual environment
# python -m venv .venv to create the virtual environment
# pip install -r requirements.txt to install the required packages
# pip freeze > requirements.txt to save the installed packages
# pip install scraper
# pip python main.py
# https://www.cnn.com/2025/03/27/Tv/video/sitroom-blitzer-rounds-signal-trump-leak
# ¿Quieres que agregue el nombre del subreddit o la fecha del post también? Puedo añadirlo en un segundo.

import asyncio
import pandas as pd
from playwright.async_api import async_playwright

async def scrape_reddit_old():
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set to True to run headless
        page = await browser.new_page()

        print("🔎 Searching Reddit (old version) for 'Trump'...")
        await page.goto("https://old.reddit.com/search?q=trump", timeout=60000)
        await page.wait_for_selector("div.search-result", timeout=15000)

        posts = await page.query_selector_all("div.search-result")
        print(f"Found {len(posts)} results. Extracting top 10...\n")

        for i, post in enumerate(posts[:20]):
            try:
                # Title and URL
                title_el = await post.query_selector("a.search-title")
                title = await title_el.inner_text()
                url = await title_el.get_attribute("href")

                # Preview text – just one line
                preview_el = await post.query_selector("div.search-expando")
                preview_raw = await preview_el.inner_text() if preview_el else ""
                preview_line = preview_raw.strip().split("\n")[0] if preview_raw else ""

                # Subreddit
                subreddit_el = await post.query_selector("a.search-subreddit-link")
                subreddit = await subreddit_el.inner_text() if subreddit_el else "unknown"

                # Date
                time_el = await post.query_selector("time")
                post_time = await time_el.inner_text() if time_el else "unknown"

                # Print to console
                print(f"POST #{i+1}")
                print(f"Title: {title}")
                print(f"URL: {url}")
                print(f"Subreddit: {subreddit}")
                print(f"Date: {post_time}")
                print(f"Preview: {preview_line}")

                # Append result
                results.append({
                    "title": title.strip(),
                    "url": url.strip(),
                    "subreddit": subreddit.strip(),
                    "date": post_time.strip(),
                    "preview_text": preview_line.strip()
                })

            except Exception as e:
                print(f"⚠️ Error in post #{i+1}: {e}")
                continue

        await browser.close()

    # Save to CSV
    df = pd.DataFrame(results)
    df.to_csv("reddit_trump_posts.csv", index=False)
    print("✅ CSV saved as 'reddit_trump_posts.csv'.")

# Run it
asyncio.run(scrape_reddit_old())