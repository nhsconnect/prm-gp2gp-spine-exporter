import io
import logging
from io import BytesIO
from os import environ
from threading import Thread

import boto3
from botocore.config import Config
from moto.server import DomainDispatcherApplication, create_backend_app
from werkzeug import Request, Response
from werkzeug.serving import make_server

from prmexporter.main import VERSION, main

FAKE_SPLUNK_HOST = "127.0.0.1"
FAKE_SPLUNK_PORT = 9000
FAKE_SPLUNK_URL = f"http://{FAKE_SPLUNK_HOST}:{FAKE_SPLUNK_PORT}"

FAKE_AWS_HOST = "127.0.0.1"
FAKE_AWS_PORT = 8887
FAKE_AWS_URL = f"http://{FAKE_AWS_HOST}:{FAKE_AWS_PORT}"
FAKE_S3_ACCESS_KEY = "testing"
FAKE_S3_SECRET_KEY = "testing"
FAKE_S3_REGION = "us-west-1"


class ThreadedServer:
    def __init__(self, server):
        self._server = server
        self._thread = Thread(target=server.serve_forever)

    def start(self):
        self._thread.start()

    def stop(self):
        self._server.shutdown()
        self._thread.join()


def _read_csv(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            yield line


@Request.application
def fake_splunk_application(request):
    return Response(_read_csv("../data/daily_spine_data.csv"), mimetype="text/csv")


def _build_fake_s3(host, port):
    app = DomainDispatcherApplication(create_backend_app)
    server = make_server(host, port, app)
    return ThreadedServer(server)


def _build_fake_splunk(host, port):
    server = make_server(host, port, fake_splunk_application)
    return ThreadedServer(server)


def _disable_werkzeug_logging():
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)


def _read_s3_csv_file(bucket, key):
    f = BytesIO()
    bucket.download_fileobj(key, f)
    wrapper = io.TextIOWrapper(f, encoding="utf-8")
    return wrapper.read()


def _read_s3_metadata(bucket, key):
    return bucket.Object(key).get()["Metadata"]


def _populate_ssm_parameter(name, value):
    ssm = boto3.client(service_name="ssm", endpoint_url=FAKE_AWS_URL)
    ssm.put_parameter(Name=name, Value=value, Type="SecureString")


def test_with_s3():
    _disable_werkzeug_logging()

    s3 = boto3.resource(
        "s3",
        endpoint_url=FAKE_AWS_URL,
        aws_access_key_id=FAKE_S3_ACCESS_KEY,
        aws_secret_access_key=FAKE_S3_SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name=FAKE_S3_REGION,
    )

    output_bucket_name = "prm-gp2gp-spine-data"
    api_token_param_name = "test/splunk/api-token"

    environ["AWS_ACCESS_KEY_ID"] = "testing"
    environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    environ["AWS_DEFAULT_REGION"] = "us-west-1"

    environ["SPLUNK_URL"] = FAKE_SPLUNK_URL
    environ["OUTPUT_SPINE_DATA_BUCKET"] = output_bucket_name
    environ["SPLUNK_API_TOKEN_PARAM_NAME"] = api_token_param_name
    environ["S3_ENDPOINT_URL"] = FAKE_AWS_URL
    # environ["BUILD_TAG"] = "61ad1e1c"

    year = 2020
    month = 1
    day = 1

    fake_s3 = _build_fake_s3(FAKE_AWS_HOST, FAKE_AWS_PORT)
    fake_splunk = _build_fake_splunk(FAKE_SPLUNK_HOST, FAKE_SPLUNK_PORT)

    # expected_metadata = {"date-anchor": "2020-01-30T18:44:49+00:00", "build-tag": "61ad1e1c"}

    try:
        fake_s3.start()
        fake_splunk.start()

        output_bucket = s3.Bucket(output_bucket_name)
        output_bucket.create()

        output_path = f"{VERSION}/{year}/{month}/{day}/{year}-{month}-{day}_spine_messages.csv"

        _populate_ssm_parameter(api_token_param_name, "abc")

        main()

        actual = _read_s3_csv_file(output_bucket, output_path)
        expected = _read_csv("../data/daily_spine_data.csv")

        # actual_s3_metadata = _read_s3_metadata(output_bucket, output_path)

        assert actual == expected
        # assert actual_s3_metadata == expected_metadata

    finally:
        fake_splunk.stop()
        fake_s3.stop()
