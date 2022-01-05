import boto3
import requests

from prmexporter.config import SpineExporterConfig
from prmexporter.io.http_client import HttpClient
from prmexporter.io.s3 import S3DataManager
from prmexporter.io.secret_manager import SsmSecretManager
from prmexporter.search_window import SearchWindow

VERSION = "v3"


class SpineExporter:
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
    def _create_s3_key(search_window: SearchWindow) -> str:
        start_datetime = search_window.get_start_datetime()
        year = str(start_datetime.year)
        month = str(start_datetime.month).zfill(2)
        day = str(start_datetime.day).zfill(2)
        return f"{VERSION}/{year}/{month}/{day}/{year}-{month}-{day}_spine_messages.csv.gz"

    def _write_spine_data_to_s3(
        self, spine_data: bytes, s3_key: str, search_start_time: str, search_end_time: str
    ):
        output_metadata = {
            "search-start-time": search_start_time,
            "search-end-time": search_end_time,
            "build-tag": self._config.build_tag,
        }

        self._s3_data_manager.write_gzip_csv(
            data=spine_data, s3_key=s3_key, metadata=output_metadata
        )

    def run(self):
        search_window = SearchWindow.prior_to_now(number_of_days=self._config.search_number_of_days)
        search_start_time = search_window.get_start_datetime_string()
        search_end_time = search_window.get_end_datetime_string()

        spine_data = self._fetch_spine_data(
            search_start_time=search_start_time, search_end_time=search_end_time
        )
        s3_key = self._create_s3_key(search_window)
        self._write_spine_data_to_s3(
            spine_data=spine_data,
            s3_key=s3_key,
            search_start_time=search_start_time,
            search_end_time=search_end_time,
        )
