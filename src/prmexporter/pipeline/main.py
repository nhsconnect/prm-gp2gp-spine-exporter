import logging

from prmexporter.domain.http_client import HttpClient
from prmexporter.utils.io.json_formatter import JsonFormatter

logger = logging.getLogger("prmexporter")


def _setup_logger():
    logger.setLevel(logging.INFO)
    formatter = JsonFormatter()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def main():
    _setup_logger()
    http_client = HttpClient(url="https://jsonplaceholder.typicode.com/todos/1")
    response = http_client.fetch_data()
    logger.info("Success!", extra={"response": response})


if __name__ == "__main__":
    main()
