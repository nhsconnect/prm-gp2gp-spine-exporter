import logging
from os import environ

from prmexporter.config import SpineExporterConfig
from prmexporter.io.json_formatter import JsonFormatter
from prmexporter.spine_exporter import SpineExporter

logger = logging.getLogger("prmexporter")


def _setup_logger():
    logger.setLevel(logging.INFO)
    formatter = JsonFormatter()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def main():
    _setup_logger()
    config = SpineExporterConfig.from_environment_variables(environ)
    spine_exporter = SpineExporter(config)
    spine_exporter.run()


if __name__ == "__main__":
    main()
