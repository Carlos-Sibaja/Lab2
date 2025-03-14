# deactivate to deactivate the virtual environment  .venv\Scripts\deactivate
# .venv\Scripts\Activate.ps1 to activate the virtual environment
# python -m venv .venv to create the virtual environment
# pip install -r requirements.txt to install the required packages
# pip freeze > requirements.txt to save the installed packages
# pip install scraper
# pip python main.py

import requests
import csv  # Import the csv module
import json  # Import the json module
from bs4 import BeautifulSoup  # Import the BeautifulSoup class from the bs4 module
import mechanicalsoup  # Import the mechanicalsoup module
from playwright.sync_api import sync_playwright  # Import the sync_playwright class from the playwright.sync_api module  
from scrapy import Selector # Import the Selector class from the scrapy module   
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("LAB 2: Web Scraping with Python")
print("This program scrapes articles from Wikipedia based on the topic you provide.")
from Scraper import (
    scrape_wikipedia_beautifulsoup,
    scrape_wikipedia_mechanicalsoup,
    scrape_wikipedia_playwright,
    scrape_wikipedia_scrapy,
    scrape_dynamic_content,
    save_results
)

def main():
    topic = input("Which topic do you want to scrape? ")
    print("Select the scraping method:")
    print("1. BeautifulSoup")
    print("2. MechanicalSoup")
    print("3. Playwright")
    print("4. Scrapy")
    print("5. Selenium (Dynamic Content)")
    print("6. All (Run all methods)")
    choice = input("Enter the number (1-6): ")

    articles = []

    if choice == "1":
        articles = scrape_wikipedia_beautifulsoup(topic)
    elif choice == "2":
        articles = scrape_wikipedia_mechanicalsoup(topic)
    elif choice == "3":
        articles = scrape_wikipedia_playwright(topic)
    elif choice == "4":
        articles = scrape_wikipedia_scrapy(topic)
    elif choice == "5":
        articles = scrape_dynamic_content(topic)
    elif choice == "6":
        print("Running all scrapers...")
        articles.extend(scrape_wikipedia_beautifulsoup(topic))
        articles.extend(scrape_wikipedia_mechanicalsoup(topic))
        articles.extend(scrape_wikipedia_playwright(topic))
        articles.extend(scrape_wikipedia_scrapy(topic))
        articles.extend(scrape_dynamic_content(topic))
    else:
        print("Invalid choice. Exiting.")
        return
    
    if articles:
        save_results(articles, filename=f"output_{topic}")
    else:
        print("No articles found.")

if __name__ == "__main__":
    main()