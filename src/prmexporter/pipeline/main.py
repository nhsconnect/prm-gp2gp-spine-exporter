import logging

from prmexporter.utils.io.json_formatter import JsonFormatter
from src.prmexporter.pipeline.make_api_call import make_api_call

logger = logging.getLogger("prmexporter")


def _setup_logger():
    logger.setLevel(logging.INFO)
    formatter = JsonFormatter()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def main() -> int:
    _setup_logger()
    response = make_api_call("https://jsonplaceholder.typicode.com/todos/1")
    logger.info("Success!", extra={"response": response})
    return 1


if __name__ == "__main__":
    main()
