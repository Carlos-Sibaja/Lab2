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
        # Launch a visible Chromium browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print("🔎 Searching Reddit (old.reddit.com) for 'Trump'...")
        # Navigate to the old Reddit search page
        await page.goto("https://old.reddit.com/search?q=trump", timeout=60000)

        # Wait until search results are visible
        await page.wait_for_selector("div.search-result", timeout=15000)

        # Get all search result containers
        posts = await page.query_selector_all("div.search-result")
        print(f"🔍 Found {len(posts)} results. Extracting top 10...\n")

        # Loop through the first 10 posts
        for i, post in enumerate(posts[:10]):
            try:
                # Get the title element
                title_el = await post.query_selector("a.search-title")
                title = await title_el.inner_text()

                # Get the URL (relative or absolute)
                url = await title_el.get_attribute("href")

                # Get the post date as shown on Reddit
                time_el = await post.query_selector("time")
                post_time = await time_el.inner_text() if time_el else "unknown"

                # Print each result to the console
                print(f"{i+1}: Title: {title}")
                print(f"   Date: {post_time}")
                print(f"   URL: {url}\n")

                # Add to results list
                results.append({
                    "title": title.strip(),
                    "url": url.strip(),
                    "date": post_time.strip()
                })

            except Exception as e:
                print(f"⚠️ Skipping post #{i+1} due to error: {e}")
                continue

        await browser.close()

    # Save results to CSV
    df = pd.DataFrame(results)
    df.to_csv("reddit_trump_posts.csv", index=False)
    print("✅ CSV saved as 'reddit_trump_posts.csv'.")

# Run the scraper
asyncio.run(scrape_reddit_old())