import logging

from prmexporter.utils.io.json_formatter import JsonFormatter

logger = logging.getLogger("prmcalculator")


def _setup_logger():
    logger.setLevel(logging.INFO)
    formatter = JsonFormatter()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def main() -> int:
    _setup_logger()
    logging.info("Hello world")
    return 1


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
