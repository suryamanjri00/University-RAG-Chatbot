# app/scrape_website.py
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

# Change this to your site’s sitemap or URL list
SITEMAP_URL = "https://university.edu/sitemap.xml"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "cleaned_texts")

def fetch_sitemap_urls(sitemap_url: str) -> list[str]:
    resp = requests.get(sitemap_url)
    soup = BeautifulSoup(resp.text, "xml")
    return [loc.text for loc in soup.find_all("loc")]

def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    # drop scripts/styles
    for tag in soup(["script","style","nav","footer","header","aside"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    # remove excess whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n\n".join(lines)

def scrape_and_save():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    urls = fetch_sitemap_urls(SITEMAP_URL)
    for url in urls:
        # optional filter: only pages with “data-science” in path
        if "data-science" not in url:
            continue
        try:
            r = requests.get(url, timeout=10)
            txt = clean_html(r.text)
            fname = re.sub(r'\W+', '_', url)[:100] + ".txt"
            with open(os.path.join(OUTPUT_DIR, fname), "w", encoding="utf-8") as f:
                f.write(txt)
            print(f"Saved {url} → {fname}")
        except Exception as e:
            print(f"Failed {url}: {e}")

if __name__ == "__main__":
    scrape_and_save()
