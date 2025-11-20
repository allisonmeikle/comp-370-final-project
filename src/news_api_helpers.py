import json
import hashlib
import os
import requests
import time

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", ".cache")
# no cache expiry for now
CACHE_EXPIRY = float("inf")
UUID_CACHE = os.path.join(os.path.dirname(__file__), "..", "data", ".cache", "uuid_cache.json")

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

def get_uuid_response(query_url):
    if not os.path.exists(UUID_CACHE):
        with open(UUID_CACHE, 'w') as fp:
            json.dump({}, fp)
    with open(UUID_CACHE, 'r') as fp:
        cached_articles = json.load(fp)

    uuid = (query_url.split('/')[-1]).split("?")[0]
    print(uuid)
    if uuid in cached_articles:
        return cached_articles[uuid]
    else:
        r = requests.get(query_url)
        r.raise_for_status()
        response = r.json()
        cached_articles[uuid] = response
        with open(UUID_CACHE, "w") as fp:
            json.dump(cached_articles, fp)
        return response