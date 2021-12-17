import logging
from datetime import datetime
from os import environ
from threading import Thread

import boto3
from botocore.config import Config
from freezegun import freeze_time
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

SPINE_DATA = (
    b"""_time,conversationID,GUID,interactionID,
        messageSender,messageRecipient,messageRef,jdiEvent,toSystem,fromSystem"""
    b"""2019-12-01T08:41:48.337+0000,abc,bcd,urn:nhs:names:services:gp2gp/MCCI_IN010000UK13,
        987654321240,003456789123,bcd,NONE,SupplierC,SupplierA"""
    b"""2019-12-01T18:02:29.985+0000,cde,cde,urn:nhs:names:services:gp2gp/RCMR_IN010000UK05,
        123456789123,003456789123,NotProvided,NONE"""
    b"""019-12-01T18:03:21.908+0000,cde,efg,urn:nhs:names:services:gp2gp/RCMR_IN030000UK06,
        003456789123,123456789123,NotProvided,NONE"""
)


class ThreadedServer:
    def __init__(self, server):
        self._server = server
        self._thread = Thread(target=server.serve_forever)

    def start(self):
        self._thread.start()

    def stop(self):
        self._server.shutdown()
        self._thread.join()


@Request.application
def fake_splunk_application(_):
    return Response(SPINE_DATA, mimetype="text/csv")


def _build_fake_aws(host, port):
    app = DomainDispatcherApplication(create_backend_app)
    server = make_server(host, port, app)
    return ThreadedServer(server)


def _build_fake_splunk(host, port):
    server = make_server(host, port, fake_splunk_application)
    return ThreadedServer(server)


def _disable_werkzeug_logging():
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)


def _read_s3_csv_file(s3_client, bucket, key):
    s3_object = s3_client.Object(bucket, key)
    response = s3_object.get()
    return response["Body"].read().decode("utf-8")


def _populate_ssm_parameter(name, value):
    ssm = boto3.client(service_name="ssm", endpoint_url=FAKE_AWS_URL)
    ssm.put_parameter(Name=name, Value=value, Type="SecureString")


@freeze_time(datetime(year=2021, month=11, day=13, hour=2, second=0))
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

    year = 2021
    month = 11
    day = 13

    fake_aws = _build_fake_aws(FAKE_AWS_HOST, FAKE_AWS_PORT)
    fake_splunk = _build_fake_splunk(FAKE_SPLUNK_HOST, FAKE_SPLUNK_PORT)

    try:
        fake_aws.start()
        fake_splunk.start()

        output_bucket = s3.Bucket(output_bucket_name)
        output_bucket.create()

        output_path = f"{VERSION}/{year}/{month}/{day}/{year}-{month}-{day}_spine_messages.csv"

        _populate_ssm_parameter(api_token_param_name, "abc")

        main()

        expected = SPINE_DATA.decode("utf-8")
        actual = _read_s3_csv_file(s3, output_bucket_name, output_path)

        assert actual == expected

    finally:
        fake_splunk.stop()
        fake_aws.stop()
