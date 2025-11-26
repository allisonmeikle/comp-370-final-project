#!/usr/bin/env python3
import argparse
import csv
import os
import requests
import time   

BASE_URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
API_KEY = "cgFMzpFtUQWh6RCMHArWcEp8frt4BH4Y"
PAGE_SIZE = 10  # NYT Article Search returns 10 docs per page

CSV_FIELDS = [
    "title",
    "description",
    "source",
    "date",
]


def fetch_articles(query: str, num_results: int, sort: str):
    """
    Fetch up to num_results articles from the NYT Article Search API.
    sort should be 'newest', 'oldest', or 'relevance'.
    """
    articles = []
    page = 0  # NYT pages are 0-based

    while len(articles) < num_results:
        # Search in abstract OR headline for the query
        if page > 0:
            time.sleep(12)
        
        fq = f'timesTag.person.contains:("{query}")'

        params = {
            "fq": fq,
            "sort": sort,
            "page": page,
            "api-key": API_KEY,
            "begin_date": 20240101,
            "end_date": 20251125,
        }

        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        docs = data.get("response", {}).get("docs", [])
        if not docs:
            break  # no more results

        for doc in docs:
            title = doc.get("headline", {} ).get("main", "")

            abstract = doc.get("abstract")

            article = {
                "title": title,
                "description": abstract,
                "source": "nytimes.com",
                "date": doc.get("pub_date", ""),
            }
            articles.append(article)

            if len(articles) >= num_results:
                break

        page += 1

    return articles[:num_results]


def append_to_csv(out_path: str, rows):
    """
    Append rows (list of dicts) to out_path.
    Writes a header if the file does not yet exist or is empty.
    """
    file_exists_and_nonempty = os.path.exists(out_path) and os.path.getsize(out_path) > 0

    with open(out_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if not file_exists_and_nonempty:
            writer.writeheader()
        writer.writerows(rows)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Query the NYT Article Search API and append results to a CSV."
    )
    parser.add_argument(
        "-q",
        "--query",
        required=True,
        help='Search query string (e.g. "Carney").',
    )
    parser.add_argument(
        "-n",
        "--num-results",
        type=int,
        required=True,
        help="Number of results to fetch and append.",
    )
    parser.add_argument(
        "-o",
        "--out",
        default="out.csv",
        help="Output CSV file (default: out.csv).",
    )
    parser.add_argument(
        "--sort",
        choices=["newest", "relevance", "oldest"],
        default="newest",
        help="NYT 'sort' parameter (default: newest).",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    articles = fetch_articles(
        query=args.query,
        num_results=args.num_results,
        sort=args.sort,
    )

    if not articles:
        print("No articles returned from the NYT API.")
        return

    append_to_csv(args.out, articles)
    print(f"Appended {len(articles)} articles to {args.out}")


if __name__ == "__main__":
    main()
