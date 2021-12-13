import logging
from os import environ

import boto3

from prmexporter.config import SpineExporterConfig
from prmexporter.http_client import HttpClient
from prmexporter.secret_manager import SsmSecretManager
from prmexporter.utils.io.json_formatter import JsonFormatter

logger = logging.getLogger("prmexporter")


def _setup_logger():
    logger.setLevel(logging.INFO)
    formatter = JsonFormatter()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


VERSION = "v3"


def main():
    _setup_logger()

    config = SpineExporterConfig.from_environment_variables(environ)

    ssm = boto3.client("ssm")
    secret_manager = SsmSecretManager(ssm)
    splunk_api_token = secret_manager.get_secret(config.splunk_api_token_param_name)

    http_client = HttpClient(url=config.splunk_url)
    api_response_content = http_client.fetch_data(auth_token=splunk_api_token)

    s3_client = boto3.resource("s3")
    s3_client.upload_fileobj(
        api_response_content, config.output_bucket, f"{VERSION}/test-spine-data.csv"
    )


if __name__ == "__main__":
    main()
