import json
import hashlib
import os
import requests
import time

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", ".cache")
# no cache expiry for now
CACHE_EXPIRY = float("inf")

def get_all_news_response(query_url):
    os.makedirs(CACHE_DIR, exist_ok=True)
    file_name = f"news_api_request_{hashlib.md5(query_url.encode('utf-8')).hexdigest()}.json"
    path = os.path.join(CACHE_DIR, file_name)

    if os.path.exists(path):
        age = time.time() - os.path.getmtime(path)
        if age < CACHE_EXPIRY:
            with open(path, 'r', encoding='utf-8') as f:
                response = f.read()
    else: 
        r = requests.get(query_url)
        r.raise_for_status()
        response = r.json()
        
        with open(path, "w") as f:
            json.dump(response, f)

    return response