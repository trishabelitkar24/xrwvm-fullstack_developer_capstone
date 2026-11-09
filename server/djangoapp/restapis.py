
import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

backend_url = os.getenv(
    'backend_url',
    default="http://localhost:3030"
)

sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    request_url = backend_url + endpoint

    try:
        response = requests.get(request_url, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        logger.error("Backend GET request failed: %s", error)
        return None


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text

    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        logger.error("Sentiment analysis request failed: %s", error)
        return None


def post_review(data_dict):
    try:
        response = requests.post(
            backend_url + "/insert_review",
            json=data_dict
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        logger.error("Review submission failed: %s", error)
        return None
