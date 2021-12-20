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
from prmexporter.io.time_calculator import TimeCalculator

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

    ssm = boto3.client("ssm", endpoint_url=config.aws_endpoint_url)
    secret_manager = SsmSecretManager(ssm)
    splunk_api_token = secret_manager.get_secret(config.splunk_api_token_param_name)

    time_calculator = TimeCalculator()
    yesterday_midnight = time_calculator.get_yesterday_midnight_datetime_string()
    today_midnight = time_calculator.get_today_midnight_datetime_string()

    output_metadata = {
        "search-start-time": yesterday_midnight,
        "search-end-time": today_midnight,
        "build-tag": config.build_tag,
    }

    data = {
        "output_mode": "csv",
        "earliest_time": yesterday_midnight,
        "latest_time": today_midnight,
        "search": """search index=\"spine2vfmmonitor\" service=\"gp2gp\" logReference=\"MPS0053d\"
        | table _time, conversationID, GUID, interactionID, messageSender,
        messageRecipient, messageRef, jdiEvent, toSystem, fromSystem""",
    }

    http_client = HttpClient(client=requests)
    api_response_content = http_client.fetch_data(
        url=config.splunk_url, auth_token=splunk_api_token, request_body=data
    )

    s3_client = boto3.resource("s3", endpoint_url=config.aws_endpoint_url)
    s3_manager = S3DataManager(client=s3_client, bucket_name=config.output_spine_data_bucket)

    year = time_calculator.get_year()
    month = time_calculator.get_month()
    day = time_calculator.get_day()

    s3_manager.write_csv(
        data=BytesIO(api_response_content),
        s3_key=f"{VERSION}/{year}/{month}/{day}/{year}-{month}-{day}_spine_messages.csv",
        metadata=output_metadata,
    )


if __name__ == "__main__":
    main()
