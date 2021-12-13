import logging

import requests

logger = logging.getLogger("prmexporter")


class HttpClientException(Exception):
    pass


class HttpClient:
    def __init__(self, url: str, client=requests):
        self._url = url
        self._client = client

    def fetch_data(self, auth_token: str) -> bytes:
        logger.info("Attempting to fetch data from: " + self._url)

        headers = {"Authorization": f"Bearer {auth_token}"}
        data = {
            "output_mode": "csv",
            "earliest_time": 1638835200,
            "latest_time": 1638921600,
            "search": """search index=\"spine2vfmmonitor\" service=\"gp2gp\" logReference=\"MPS0053d\"
            | head 1
            | table _time, conversationID, GUID, interactionID, messageSender,
            messageRecipient, messageRef, jdiEvent, toSystem, fromSystem""",
        }
        response = self._client.post(url=self._url, data=data, headers=headers)

        if response.status_code != 200:
            raise HttpClientException(
                f"Unable to fetch data from {self._url} with status code: {response.status_code}"
            )

        logger.info(
            "Successfully fetched data from splunk",
            extra={"Response content": str(response.content)},
        )

        return response.content
