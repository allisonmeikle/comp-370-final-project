import argparse
import json
import os

from news_api_helpers import get_all_news_response

from dotenv import load_dotenv

BASE_URL = "https://api.thenewsapi.com/v1/news/all"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("political_figure", type=str, help="Name of the political figure to extract articles for.")
    parser.add_argument("-n", type = int, help="Number of articles to extract")
    # take in domain id list

    # extract articles, header and description line based on what number of it says, ten extra for each so we have room to reject
    # for the request, sort by date latest to oldest
    # add to csv store title, author, publication, date, description
    

    args = parser.parse_args()

    n = args.n or 500
    load_dotenv()
    NEWS_API_TOKEN = os.getenv("NEWS_API_TOKEN")
    if not NEWS_API_TOKEN:
        raise RuntimeError(f"Could not find an API token to use in the .env file")
    
    name = args.political_figure.replace(" ", "%20")
    query_url = BASE_URL + f'?api_token={NEWS_API_TOKEN}&language=en&limit={n}&search="{name}"'
    response = get_all_news_response(query_url)
    response_json = json.loads(response)
    
    articles = {}
    for article in response_json["data"]:
        print(article)
    
if __name__ == "__main__":
    main()