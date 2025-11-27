from bs4 import BeautifulSoup
import csv
import argparse
from pathlib import Path

def parse_ctv(html_path):
    # html_path is a file path; read the HTML from disk
    html_path = Path(html_path)
    html = html_path.read_text(encoding="utf-8")

    soup = BeautifulSoup(html, "html.parser")
    rows = []

    last_date = ""

    # each result has title + description + date in the same block
    for card in soup.select("div.card.search"):
        # date/time
        date_tag = card.select_one("p.date-time.mb-1.mb-lg-0.card-text")
        date_str = last_date 
        if date_tag:
            text = date_tag.get_text(strip=True)
            if text:                 # only update if not empty
                date_str = text
                last_date = text

        # title
        title_tag = card.select_one("div.card-title")
        title = title_tag.get_text(strip=True) if title_tag else ""

        # description / excerpt
        desc_tag = card.select_one("div.card-description p.card-text")
        description = desc_tag.get_text(strip=True) if desc_tag else ""

        rows.append([title, description, "citynews.ca", date_str])

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

    print(f"Found {len(rows)} articles, appended to {out_path}")

if __name__ == "__main__":
    main()
