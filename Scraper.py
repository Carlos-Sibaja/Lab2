#pip install requests
#pip install requests beautifulsoup4 mechanicalsoup playwright scrapy selenium

import requests
import csv
import json
from bs4 import BeautifulSoup
import mechanicalsoup
from playwright.sync_api import sync_playwright
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/{}"

# -------------------------- BEAUTIFULSOUP SCRAPER --------------------------
def scrape_wikipedia_beautifulsoup(topic, max_articles=10):
    url = WIKIPEDIA_URL.format(topic.replace(" ", "_"))
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    print(soup.prettify())  # Debug: Check the HTML structure

    articles = []
    for item in soup.find_all("p")[:max_articles]:
        text = item.get_text(strip=True)
        if text:
            articles.append({
                "text": text,
                "source": "BeautifulSoup"
            })
    
    return articles

# -------------------------- MECHANICALSOUP SCRAPER --------------------------
def scrape_wikipedia_mechanicalsoup(topic, max_articles=10):
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(WIKIPEDIA_URL.format(topic.replace(" ", "_")))
    soup = browser.page
    
    articles = []
    for item in soup.find_all("p")[:max_articles]:
        text = item.get_text(strip=True)
        if text:
            articles.append({
                "text": text,
                "source": "MechanicalSoup"
            })
    
    return articles

# -------------------------- PLAYWRIGHT SCRAPER --------------------------
def scrape_wikipedia_playwright(topic, max_articles=10):
    articles = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(WIKIPEDIA_URL.format(topic.replace(" ", "_")))
        
        page.wait_for_selector("p")
        elements = page.query_selector_all("p")
        
        for item in elements[:max_articles]:
            text = item.inner_text()
            if text:
                articles.append({
                    "text": text,
                    "source": "Playwright"
                })
        
        browser.close()
    
    return articles

# -------------------------- SCRAPY SCRAPER --------------------------
def scrape_wikipedia_scrapy(topic, max_articles=10):
    url = WIKIPEDIA_URL.format(topic.replace(" ", "_"))
    response = requests.get(url)
    selector = Selector(text=response.text)
    
    articles = []
    for item in selector.css("p")[:max_articles]:
        text = item.css("::text").get()
        if text:
            articles.append({
                "text": text,
                "source": "Scrapy"
            })
    
    return articles

# -------------------------- SAVE RESULTS --------------------------
def save_results(articles, filename="output"):
    """Saves scraped results as CSV and JSON."""
    
    if not articles:
        print("❌ No results to save.")
        return
    
    # Save as CSV
    with open(f"{filename}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["source", "text"])
        writer.writeheader()
        writer.writerows(articles)
    
    # Save as JSON
    with open(f"{filename}.json", "w", encoding="utf-8") as file:
        json.dump(articles, file, indent=4, ensure_ascii=False)

    print(f"✅ Results saved in {filename}.csv and {filename}.json")

   # -------------------------- DYNAMIC CONTENT SCRAPER --------------------------
def scrape_dynamic_content(topic, max_articles=10):
    """Scrapes Wikipedia for the given topic and returns up to max_articles paragraphs with the URL."""
    
    # Initialize WebDriver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(service=service, options=options)

    # Format URL
    url = WIKIPEDIA_URL.format(topic.replace(" ", "_"))
    driver.get(url)
    
    # Wait for content to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a"))
        )
    except:
        print(f"❌ Error: Could not load content for {topic}")
        driver.quit()
        return []

    # Parse HTML
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    articles = []
    for item in soup.find_all("a")[:max_articles]:
        text = item.get_text(strip=True)
        if text:
            articles.append({
                "source": url,
                "text": text
            })
    
    print(soup.prettify())  # Debug: Check the HTML structure
    return articles