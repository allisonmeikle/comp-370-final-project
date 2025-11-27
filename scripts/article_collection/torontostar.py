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

    # each search result card
    for art in soup.select("article.card.summary"):
        # title
        title_tag = art.select_one(".card-headline a.tnt-asset-link")
        if not title_tag:
            continue  # skip weird cards
        title = title_tag.get_text(strip=True)

        # excerpt / summary
        excerpt_tag = art.select_one(".card-lead .tnt-summary")
        excerpt = excerpt_tag.get_text(strip=True) if excerpt_tag else ""

        # date: prefer datetime attribute, fall back to text,
        # and if totally missing, reuse previous article's date
        time_tag = art.select_one("li.card-date time")
        date_str = last_date  # default = previous date

        if time_tag:
            dt_attr = (time_tag.get("datetime") or "").strip()
            text = time_tag.get_text(strip=True)
            if dt_attr:
                date_str = dt_attr
            elif text:
                date_str = text

        if date_str:      # update last_date only if we actually have something
            last_date = date_str

        rows.append([title, excerpt, "thestar.com", date_str])

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
