#!/usr/bin/env python3
import argparse
import csv
import os
import requests

BASE_URL = "https://content.guardianapis.com/search"
API_KEY = "73918735-bdfc-46cc-9e50-d295298dc18c"
PAGE_SIZE = 50 

CSV_FIELDS = [
    "title",
    "description",
    "source",
    "date",
]


def fetch_articles(query: str, num_results: int, order_by: str):
    """
    Fetch up to num_results articles from the Guardian Content API.
    order_by should be 'newest' or 'relevance'.
    """
    articles = []
    page = 1

    while len(articles) < num_results:
        params = {
            "q": query,
            "order-by": order_by,
            "page": page,
            "page-size": PAGE_SIZE,
            "api-key": API_KEY,
            "show-fields": "headline,trailText",
            "query-fields": "headline,trailText",
        }

        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        results = data.get("response", {}).get("results", [])
        if not results:
            break  # no more results

        for res in results:
            article = {
                "title": res.get("fields", {}).get("headline", ""),
                "description": res.get("fields", {}).get("trailText", ""),
                "source": "theguardian.com",
                "date": res.get("webPublicationDate", ""),
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
        description="Query the Guardian Content API and append results to a CSV."
    )
    parser.add_argument(
        "-q",
        "--query",
        required=True,
        help='Search query string (e.g. "carney").',
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
        "--order-by",
        choices=["newest", "relevance"],
        default="newest",
        help="Guardian 'order-by' parameter (default: newest).",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    articles = fetch_articles(
        query=args.query,
        num_results=args.num_results,
        order_by=args.order_by,
    )

    if not articles:
        print("No articles returned from the Guardian API.")
        return

    append_to_csv(args.out, articles)
    print(f"Appended {len(articles)} articles to {args.out}")


if __name__ == "__main__":
    main()
