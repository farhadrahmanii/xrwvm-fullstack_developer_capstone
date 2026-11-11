import os
from urllib.parse import quote

import requests
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030").rstrip('/')
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url', default="http://localhost:5050/")
if not sentiment_analyzer_url.endswith('/'):
    sentiment_analyzer_url += '/'


def get_request(endpoint, **kwargs):
    request_url = backend_url + endpoint
    print("GET from {}".format(request_url))
    try:
        response = requests.get(request_url, params=kwargs, timeout=15)
        return response.json()
    except Exception as err:
        print("Network exception occurred: {}".format(err))
        return None


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + quote(str(text))
    try:
        response = requests.get(request_url, timeout=15)
        return response.json()
    except Exception as err:
        print("Sentiment analyzer error: {}".format(err))
        return {"sentiment": "neutral"}


def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    response = requests.post(request_url, json=data_dict, timeout=15)
    return response.json()
