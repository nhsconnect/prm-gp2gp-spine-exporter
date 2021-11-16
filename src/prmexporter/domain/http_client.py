import json

import requests


class HttpClient:
    def __init__(self, url, client=requests):
        self._url = url
        self._client = client

    def fetch_data(self):
        response = self._client.get(self._url)
        return json.loads(response.content)
