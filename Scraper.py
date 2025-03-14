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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CNN_URL = "https://edition.cnn.com/search?q={}&size=10&page=1"

# -------------------------- BEAUTIFULSOUP SCRAPER --------------------------
def scrape_cnn_beautifulsoup(topic, max_articles=10):
    url = CNN_URL.format(topic.replace(" ", "%20"))
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    print(soup.prettify())  # Debug: Check the HTML structure

    articles = []
    for item in soup.find_all("div", class_="cnn-search__result-contents")[:max_articles]:
        title = item.find("h3", class_="cnn-search__result-headline")
        link = item.find("a", href=True)
        if title and link:
            articles.append({
                "title": title.get_text(strip=True),
                "url": "https://edition.cnn.com" + link["href"],
                "source": "BeautifulSoup"
            })
    
    return articles

# -------------------------- MECHANICALSOUP SCRAPER --------------------------
def scrape_cnn_mechanicalsoup(topic, max_articles=10):
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(CNN_URL.format(topic.replace(" ", "%20")))
    soup = browser.page
    
    articles = []
    for item in soup.find_all("h3", class_="cnn-search__result-headline")[:max_articles]:
        title = item.get_text()
        link = "https://edition.cnn.com" + item.a["href"] if item.a else ""
        articles.append({"title": title, "url": link, "source": "MechanicalSoup"})
    
    return articles

# -------------------------- PLAYWRIGHT SCRAPER --------------------------
def scrape_cnn_playwright(topic, max_articles=10):
    articles = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(CNN_URL.format(topic.replace(" ", "%20")))
        
        page.wait_for_selector("h3.cnn-search__result-headline")
        elements = page.query_selector_all("h3.cnn-search__result-headline")
        
        for item in elements[:max_articles]:
            title = item.inner_text()
            link = "https://edition.cnn.com" + item.query_selector("a").get_attribute("href")
            articles.append({"title": title, "url": link, "source": "Playwright"})
        
        browser.close()
    
    return articles

# -------------------------- SCRAPY SCRAPER --------------------------
def scrape_cnn_scrapy(topic, max_articles=10):
    url = CNN_URL.format(topic.replace(" ", "%20"))
    response = requests.get(url)
    selector = Selector(text=response.text)
    
    articles = []
    for item in selector.css("h3.cnn-search__result-headline")[:max_articles]:
        title = item.css("::text").get()
        link = "https://edition.cnn.com" + item.css("a::attr(href)").get()
        articles.append({"title": title, "url": link, "source": "Scrapy"})
    
    return articles

# -------------------------- SAVE RESULTS --------------------------
def save_results(articles, filename="output"):
    # Save as CSV
    with open(f"{filename}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["source", "title", "url"])
        writer.writeheader()
        writer.writerows(articles)
    
    # Save as JSON
    with open(f"{filename}.json", "w", encoding="utf-8") as file:
        json.dump(articles, file, indent=4, ensure_ascii=False)

    print(f"Results saved in {filename}.csv and {filename}.json")

# -------------------------- DYNAMIC CONTENT SCRAPER --------------------------
def scrape_dynamic_content(topic, max_articles=10):
    driver_path = "path/to/chromedriver"  # Replace with the actual path to your ChromeDriver executable
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode
    driver = webdriver.Chrome(service=service, options=options)
    
    url = CNN_URL.format(topic.replace(" ", "%20"))
    driver.get(url)
    
    # Wait for the search results to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.cnn-search__result-contents"))
    )
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    
    articles = []
    for item in soup.find_all("div", class_="cnn-search__result-contents")[:max_articles]:
        title = item.find("h3", class_="cnn-search__result-headline")
        link = item.find("a", href=True)
        if title and link:
            articles.append({
                "title": title.get_text(strip=True),
                "url": "https://edition.cnn.com" + link["href"],
                "source": "Selenium"
            })
    
    return articles