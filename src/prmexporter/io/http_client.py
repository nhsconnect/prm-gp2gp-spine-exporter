import logging
from typing import Optional

logger = logging.getLogger("prmexporter")


class HttpClientException(Exception):
    pass


class HttpClient:
    def __init__(self, client):
        self._client = client

    def fetch_data(self, url: str, auth_token: str, request_body: Optional[object] = None) -> bytes:
        logger.info("Attempting to fetch data from: " + url)

        headers = {"Authorization": f"Bearer {auth_token}"}
        response = self._client.post(url=url, data=request_body, headers=headers)

        if response.status_code != 200:
            raise HttpClientException(
                f"Unable to fetch data from {url} with status code: {response.status_code}"
            )

        logger.info(
            "Successfully fetched data from: " + url,
        )

        return response.content
