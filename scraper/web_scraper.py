import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    """Scrapes text content from a given URL."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        return " ".join([p.text for p in soup.find_all("p")])[:2000]  # Limit to 2000 chars
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return ""
