import json
import logging

import requests

logger = logging.getLogger("prmexporter")


class HttpClientException(Exception):
    pass


class HttpClient:
    def __init__(self, url: str, client=requests):
        self._url = url
        self._client = client

    def fetch_data(self, auth_token: str) -> object:
        logger.info("Attempting to fetch data from: " + self._url)

        headers = {"Accept": "application/json", "Authorization": f"Bearer {auth_token}"}
        response = self._client.get(url=self._url, headers=headers)

        if response.status_code != 200:
            raise HttpClientException(
                f"Unable to fetch data from {self._url} with status code: {response.status_code}"
            )

        logger.info("Successfully fetched data from splunk", extra={"response": str(response)})

        return json.loads(response.content)
