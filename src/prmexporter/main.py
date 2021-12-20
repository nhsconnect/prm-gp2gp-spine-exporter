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


class SpineExporterPipeline:
    def __init__(self, config: SpineExporterConfig):
        self._config = config

        ssm = boto3.client("ssm", endpoint_url=config.aws_endpoint_url)
        self._ssm_secret_manager = SsmSecretManager(ssm)

        s3_client = boto3.resource("s3", endpoint_url=config.aws_endpoint_url)
        self._s3_data_manager = S3DataManager(
            client=s3_client, bucket_name=config.output_spine_data_bucket
        )

        self._http_client = HttpClient(client=requests)

    def _get_api_auth_token(self) -> str:
        return self._ssm_secret_manager.get_secret(self._config.splunk_api_token_param_name)

    def _fetch_spine_data(self, search_start_time: str, search_end_time: str) -> bytes:
        request_body = {
            "output_mode": "csv",
            "earliest_time": search_start_time,
            "latest_time": search_end_time,
            "search": """search index=\"spine2vfmmonitor\" service=\"gp2gp\" logReference=\"MPS0053d\"
            | table _time, conversationID, GUID, interactionID, messageSender,
            messageRecipient, messageRef, jdiEvent, toSystem, fromSystem""",
        }

        splunk_api_token = self._get_api_auth_token()

        return self._http_client.make_request(
            url=self._config.splunk_url, auth_token=splunk_api_token, request_body=request_body
        )

    @staticmethod
    def _get_s3_key(time_calculator: TimeCalculator) -> str:
        year = time_calculator.get_year()
        month = time_calculator.get_month()
        day = time_calculator.get_day()
        return f"{VERSION}/{year}/{month}/{day}/{year}-{month}-{day}_spine_messages.csv"

    def _write_spine_data_to_s3(
        self, spine_data: bytes, s3_key: str, search_start_time: str, search_end_time: str
    ):
        output_metadata = {
            "search-start-time": search_start_time,
            "search-end-time": search_end_time,
            "build-tag": self._config.build_tag,
        }

        self._s3_data_manager.write_csv(
            data=BytesIO(spine_data), s3_key=s3_key, metadata=output_metadata
        )

    def run(self):
        time_calculator = TimeCalculator()
        yesterday_midnight = time_calculator.get_yesterday_midnight_datetime_string()
        today_midnight = time_calculator.get_today_midnight_datetime_string()

        spine_data = self._fetch_spine_data(
            search_start_time=yesterday_midnight, search_end_time=today_midnight
        )
        s3_key = self._get_s3_key(time_calculator)
        self._write_spine_data_to_s3(
            spine_data=spine_data,
            s3_key=s3_key,
            search_start_time=yesterday_midnight,
            search_end_time=today_midnight,
        )


def main():
    _setup_logger()
    config = SpineExporterConfig.from_environment_variables(environ)
    pipeline = SpineExporterPipeline(config)
    pipeline.run()


if __name__ == "__main__":
    main()
