from bs4 import BeautifulSoup
import csv
import argparse
from pathlib import Path

SEARCH_URL = "https://www.ctvnews.ca/search"

def parse_ctv(html_path):
    # html_path is a file path; read the HTML from disk
    html_path = Path(html_path)
    html = html_path.read_text(encoding="utf-8")

    soup = BeautifulSoup(html, "html.parser")
    rows = []

    # each result has title + description + date in the same block
    for title_div in soup.select("div.queryly_item_title"):
        parent = title_div.parent

        title = title_div.get_text(strip=True)

        desc_div = parent.select_one("div.queryly_item_description")
        description = desc_div.get_text(strip=True) if desc_div else ""

        # date is the next div after description (like "Nov 25, 2025")
        date_div = desc_div.find_next_sibling("div") if desc_div else None
        date = date_div.get_text(strip=True) if date_div else ""

        rows.append([title, description, "ctvnews.ca", date])

    return rows

def parse_args():
    parser = argparse.ArgumentParser(
        description="fetch articles from ctv news web page"
    )
    parser.add_argument(
        "-input", "-in",              # <-- accept both -input and -in
        dest="input_path",
        required=True,
        help="Path to input html file",
    )
    parser.add_argument(
        "-out",
        dest="out_path",
        required=True,
        help="Path to output csv file",
    )
    return parser.parse_args()

def main():
    args = parse_args()
    rows = parse_ctv(args.input_path)

    out_path = Path(args.out_path)
    # append rows to out.csv (assumes header already exists)
    with out_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

    print(f"Found {len(rows)} CTV articles, appended to {out_path}")

if __name__ == "__main__":
    main()
