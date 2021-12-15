import logging
from io import BytesIO
from os import environ

import boto3
import requests

from prmexporter.config import SpineExporterConfig
from prmexporter.io.http_client import HttpClient
from prmexporter.io.json_formatter import JsonFormatter
from prmexporter.io.s3 import S3DataManager
from prmexporter.io.secret_manager import SsmSecretManager

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

    data = {
        "output_mode": "csv",
        "earliest_time": 1638316800,
        "latest_time": 1638489600,
        "search": """search index=\"spine2vfmmonitor\" service=\"gp2gp\" logReference=\"MPS0053d\"
        | table _time, conversationID, GUID, interactionID, messageSender,
        messageRecipient, messageRef, jdiEvent, toSystem, fromSystem""",
    }

    http_client = HttpClient(client=requests)
    api_response_content = http_client.fetch_data(
        url=config.splunk_url, auth_token=splunk_api_token, request_body=data
    )

    s3_client = boto3.resource("s3")
    s3_manager = S3DataManager(client=s3_client, bucket_name=config.output_spine_data_bucket)
    s3_manager.write_csv(
        data=BytesIO(api_response_content), s3_key=f"{VERSION}/test-spine-data.csv"
    )


if __name__ == "__main__":
    main()
