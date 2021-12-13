import logging
from typing import Optional

import requests

logger = logging.getLogger("prmexporter")


class HttpClientException(Exception):
    pass


class HttpClient:
    def __init__(self, url: str, client=requests):
        self._url = url
        self._client = client

    def fetch_data(self, auth_token: str, request_body: Optional[object] = None) -> bytes:
        logger.info("Attempting to fetch data from: " + self._url)

        headers = {"Authorization": f"Bearer {auth_token}"}
        response = self._client.get(url=self._url, data=request_body, headers=headers)

        if response.status_code != 200:
            raise HttpClientException(
                f"Unable to fetch data from {self._url} with status code: {response.status_code}"
            )

        logger.info(
            "Successfully fetched data from splunk",
            extra={"Response content": str(response.content)},
        )

        return response.content
