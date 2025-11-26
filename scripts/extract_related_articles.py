import argparse
import json
import os
import csv
from datetime import date
import requests
import time
import math

BASE_URL = "https://api.thenewsapi.com/v1/news/all"
DAILY_LIMIT = 3 # limit of requests each day
PAGE_SIZE = 3 # how many articles each request returns
TOKEN = "nb12MNLS0KwH5vgiFtOqjK5dPQlqHgBojFp8P6nN"


def create_search(searches):
    """
    Accepts as input every phrase the user would like 
    to query for and returns the cleaned up query
    """
    cleaned = [s.strip() for s in searches if s.strip()]
    phrases = [f'"{s}"' for s in cleaned]
    raw_query = " | ".join(phrases)
    return raw_query

def calculate_domains_today(in_path):
    """
    Given the input file, calculates how many articles we will be able to query today
    """
    remaining_rows = []
    rows_today = []
    
    with open(in_path, "r", encoding="utf-8", newline="") as in_f:
        reader = csv.reader(in_f)
        header = next(reader, None)
        if header is None:
            print("Input CSV is empty")
            return None, [], []
        rows = list(reader)
        total_requests = 0
        for row in rows:
            requests_needed = math.ceil(int(row[1])/PAGE_SIZE)
            if total_requests + requests_needed <= DAILY_LIMIT:
                total_requests = total_requests + requests_needed
                rows_today.append(row)
            else:
                remaining_rows.append(row)
    return header, rows_today, remaining_rows

def create_remaining(header, remaining):
    """
    Creates a remaining file with the domains scheduled to be queried for tomorrow
    """

    if remaining:
            remaining_path = "remaining.csv"
            with open(remaining_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(remaining)
            print(f"Remaining domains written to {remaining_path}")
    else:
        print("All domains processed within today's limit.")
    pass

def make_request(domain, page, search, sort):
    """
    Creates and executes the request given the inputted arguments
    """

    if sort == "date":
        sort_url = "published_on"
    else:
        sort_url = "relevance_score"

    params = {
        "api_token": TOKEN,
        "search": search,                        
        "search_fields": "title,description",
        "domains": domain,
        "page": page,
        "sort": sort_url,
        "language": "en",
    }

    resp = requests.get(BASE_URL, params=params)  
    return resp

def extract_articles(resp):
    """
    Executes the queries for the articles
    """

    resp.raise_for_status()
    data = resp.json()
    articles = data.get("data", [])

    rows = []
    for a in articles:
        title = a.get("title", "")
        description = a.get("description", "")
        source = a.get("source", "")       
        date = a.get("published_at", "")       

        rows.append([title, description, source, date])

    return rows

def save_articles(articles, out_path):
    """
    Writes the article information to the output csv
    """

    header = ["title", "description", "source", "date"]
    need_header = (not os.path.exists(out_path)) or os.stat(out_path).st_size == 0

    with open(out_path, "a", encoding="utf-8", newline="") as out_f:
        writer = csv.writer(out_f)

        if need_header:
            writer.writerow(header)

        for row in articles:
            writer.writerow(row)


def main():
    parser = argparse.ArgumentParser()
    

    parser.add_argument("-q", 
                        "--query", 
                        nargs="+",
                        required=True,
                        help="List of searches"
                        )

    parser.add_argument("-i", 
                        "--input_path",
                        required=True, 
                        type=str, 
                        help="Input path to csv of domain IDs that contains the domain ID and number of articles to extract"
                        )
    parser.add_argument("-o",
                        "--output_path",
                        required=True,
                        type=str,
                        help="Path to output csv that stores article information"
                        )
    parser.add_argument("-s",
                        "--sort_by", 
                        default="date", 
                        choices=["date", "relevance"], 
                        help ="Sort results by date (newest first) or relevance, default is date"
                        )

    args = parser.parse_args()


    searches = args.query
    in_path = args.input_path
    out_path = args.output_path
    sort= args.sort_by
    search = create_search(searches)

    # determining which domains we can query for today and storing the rest
    header, domains_today, remaining = calculate_domains_today(in_path)
    if header is None:
        return
    create_remaining(header, remaining)
    
    # quering for the possible domains and saving those articles
    for row in domains_today:
        domain = row[0]
        num = int(row[1])

        page = 1
        saved_for_domain = 0
        while saved_for_domain < (num):
            resp = make_request(domain, page, search, sort)
            articles = extract_articles(resp)

            if not articles:
                break

            remaining_needed = num - saved_for_domain
            to_save = articles[:remaining_needed]

            save_articles(to_save, out_path)

            saved_for_domain += len(to_save)
            page += 1

   
if __name__ == "__main__":
    main()