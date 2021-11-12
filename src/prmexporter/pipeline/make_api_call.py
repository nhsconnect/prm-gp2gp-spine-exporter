import logging

import requests

logger = logging.getLogger(__name__)


def make_api_call(url: str) -> str:
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    api_response = response.json()
    return api_response
