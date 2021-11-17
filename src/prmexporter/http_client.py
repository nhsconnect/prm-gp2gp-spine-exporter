import json

import requests


class HttpClientException(Exception):
    pass


class HttpClient:
    def __init__(self, url: str, client=requests):
        self._url = url
        self._client = client

    def fetch_data(self) -> object:
        response = self._client.get(self._url)
        if response.status_code != 200:
            raise HttpClientException(
                f"Unable to fetch data from {self._url} with status code: {response.status_code}"
            )
        return json.loads(response.content)
