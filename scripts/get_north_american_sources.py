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
    for i in range(1, 101):
        print(f"Got page {i}")
        query_url = BASE_URL + f'&api_token={NEWS_API_TOKEN}&page={i}'
        page += 1
        response = requests.get(query_url)
        response.raise_for_status()
        response_json = json.loads(response.text)
        sources["sources"].extend(response_json['data'])
        
    with open(os.path.join(SCRIPT_DIR, "..", "data", "sources.json"), "w") as f:
        json.dump(sources, f)
    
    df = pd.read_json(os.path.join(SCRIPT_DIR, "..", "data", "sources.json"))
    print(len(df))

if __name__ == "__main__":
    main()