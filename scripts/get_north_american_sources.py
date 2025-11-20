import os
import json
import requests
from dotenv import load_dotenv
import pandas as pd

BASE_URL = "https://api.thenewsapi.com/v1/news/sources?language=en"
SCRIPT_DIR = os.path.dirname(__file__)

def main():
    
    load_dotenv()
    NEWS_API_TOKEN = os.getenv("NEWS_API_TOKEN")
    if not NEWS_API_TOKEN:
        raise RuntimeError(f"Could not find an API token to use in the .env file")
    
    sources = {"sources":[]}
    page = 1
    while (page < 500):
        print(f"Got page {page}")
        query_url = BASE_URL + f'&api_token={NEWS_API_TOKEN}&page={page}'
        page += 1
        response = requests.get(query_url)
        response.raise_for_status()
        response_json = json.loads(response.text)
        sources["sources"].extend(response_json['data'])
        
        
    with open(os.path.join(SCRIPT_DIR, "..", "data", "sources", "sources.json"), "w") as f:
        json.dump(sources, f)

if __name__ == "__main__":
    main()