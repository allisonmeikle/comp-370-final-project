import argparse
import json
import os
import requests

from news_api_helpers import get_all_news_response

from dotenv import load_dotenv

BASE_URL = "https://newsapi.org/v2/everything"

def main():


    n = 500
    load_dotenv()
    NEWS_API_TOKEN = os.getenv("NEWS_API_ORG_TOKEN")
    if not NEWS_API_TOKEN:
        raise RuntimeError(f"Could not find an API token to use in the .env file")
    
    name = "Mark Carney".replace(" ", "%20")
    query_url = BASE_URL + f'?q="{name}"&apiKey={NEWS_API_TOKEN}'
    response = get_all_news_response(query_url)
    response_json = json.loads(response)
    
    articles = {}
    for article in response_json["data"]:
        print(article)
    
if __name__ == "__main__":
    main()