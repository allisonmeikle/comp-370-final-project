import argparse
import json
import os

from news_api_helpers import get_uuid_response

from dotenv import load_dotenv

BASE_URL = "https://api.thenewsapi.com/v1/news/uuid/"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", type=str, help="uuid of article to search")
    args = parser.parse_args()
    uuid = args.u
    load_dotenv()
    NEWS_API_TOKEN = os.getenv("NEWS_API_TOKEN")
    if not NEWS_API_TOKEN:
        raise RuntimeError(f"Could not find an API token to use in the .env file")
    
    query_url = BASE_URL + f'{uuid}?api_token={NEWS_API_TOKEN}'
    print(query_url)
    response = get_uuid_response(query_url)
    print(response)
    
if __name__ == "__main__":
    main()