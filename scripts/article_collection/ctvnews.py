import requests
from bs4 import BeautifulSoup
import csv
import time

SEARCH_URL = "https://www.ctvnews.ca/search" 
QUERY = "Carney"
PAGES_TO_FETCH = 5 

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; comp370-scraper/1.0; +https://example.com)"
}

def fetch_search_page(page: int) -> str:
    params = {
        "q": QUERY,
        "page": page, 
    }
    resp = requests.get(SEARCH_URL, params=params, headers=HEADERS)
    resp.raise_for_status()
    return resp.text

def parse_results(html: str):
    soup = BeautifulSoup(html, "html.parser")
    results = []

    # This selector is generic; you’ll tweak it after inspecting the HTML.
    # Start by grabbing all <a> tags that look like article links.
    for a in soup.find_all("a", href=True):
        href = a["href"]
        title = a.get_text(strip=True)

        if not title:
            continue

        # normalize relative URLs
        if href.startswith("/"):
            href = "https://www.ctvnews.ca" + href

        # keep only CTV News article links
        if "ctvnews.ca" not in href:
            continue

        results.append((title, href))

    return results

def main():
    seen_urls = set()
    all_articles = []

    for page in range(1, PAGES_TO_FETCH + 1):
        html = fetch_search_page(page)
        articles = parse_results(html)

        if not articles:
            break  # probably no more results

        for title, url in articles:
            if url in seen_urls:
                continue
            seen_urls.add(url)
            all_articles.append((title, url))

        time.sleep(1)  # be polite; don’t hammer their server

    # Save to CSV
    with open("ctv_carney_articles.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "url"])
        writer.writerows(all_articles)

if __name__ == "__main__":
    main()
