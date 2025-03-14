from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time

SEARCH_URL = "https://en.wikipedia.org/w/index.php?search={}"
BASE_URL = "https://en.wikipedia.org"

def get_wikipedia_links(topic, max_links=10):
    """Search Wikipedia for a topic and return up to max_links article URLs."""
    print(f"🔎 Searching Wikipedia for: {topic}...\n")

    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # Remove headless mode for debugging
    # options.add_argument('--headless')  
    options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(SEARCH_URL.format(topic.replace(" ", "+")))

        # Increase wait time to 20 seconds
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.mw-search-results li.mw-search-result"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        links = []

        for link in soup.select("ul.mw-search-results li.mw-search-result a")[:max_links]:
            href = link.get("href")
            full_url = BASE_URL + href
            links.append(full_url)

        print(f"✅ Found {len(links)} articles!\n")

    except Exception as e:
        print(f"❌ Error: Could not find search results. {str(e)}")
        links = []

    finally:
        driver.quit()

    return links

def scrape_wikipedia_page(url, topic):
    """Scrape a Wikipedia page and return 3 lines where the topic appears."""
    print(f"📄 Scraping: {url}")

    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Remove for debugging
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        text_snippets = []

        for paragraph in soup.find_all("p"):
            text = paragraph.get_text(strip=True)
            if topic.lower() in text.lower():
                sentences = text.split(". ")
                snippet = ". ".join(sentences[:3])  # Get 3 sentences
                text_snippets.append(snippet)
                if len(text_snippets) >= 3:
                    break

        print(f"   ✅ Extracted {len(text_snippets)} snippets.\n")

    except Exception as e:
        print(f"   ❌ Error scraping {url}: {str(e)}")
        text_snippets = []

    finally:
        driver.quit()

    return text_snippets

def main():
    topic = "Trump"  # Example topic
    max_results = 10  # Number of Wikipedia articles to scrape

    wikipedia_links = get_wikipedia_links(topic, max_results)

    if not wikipedia_links:
        print("❌ No articles found.")
        return

    results = []
    
    for idx, url in enumerate(wikipedia_links, start=1):
        snippets = scrape_wikipedia_page(url, topic)
        if snippets:
            results.append({
                "url": url,
                "snippets": snippets
            })
        
        print(f"[{idx}/{len(wikipedia_links)}] Scraped: {url} ({len(snippets)} snippets found)")
        
        time.sleep(3)  # Delay to avoid bot detection

    print("\n=== 📌 Search Results ===\n")
    for result in results:
        print(f"🔗 {result['url']}")
        for snippet in result["snippets"]:
            print(f"   📝 {snippet}\n")

if __name__ == "__main__":
    main()