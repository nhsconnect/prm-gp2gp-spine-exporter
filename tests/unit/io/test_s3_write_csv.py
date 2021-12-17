import boto3
from moto import mock_s3

from prmexporter.io.s3 import S3DataManager
from tests.builders.file import build_bytes_io_contents, build_csv_contents

MOTO_MOCK_REGION = "us-east-1"
SOME_METADATA = {"metadata_field": "metadata_value"}


@mock_s3
def test_writes_csv_to_s3():
    conn = boto3.resource("s3", region_name=MOTO_MOCK_REGION)
    bucket_name = "test_bucket"
    s3_key = "v2/fruits.csv"
    bucket = conn.create_bucket(Bucket=bucket_name)
    s3_manager = S3DataManager(client=conn, bucket_name=bucket_name)

    csv_data = build_csv_contents(
        header=["header1", "header2"],
        rows=[["row1-col1", "row1-col2"], ["row2-col1", "row2-col2"]],
    )
    data = build_bytes_io_contents(csv_data)

    expected = b"header1,header2\nrow1-col1,row1-col2\nrow2-col1,row2-col2"

    s3_manager.write_csv(data=data, s3_key=s3_key, metadata=SOME_METADATA)

    actual = bucket.Object(s3_key).get()["Body"].read()

    assert actual == expected


@mock_s3
def test_writes_metadata():
    conn = boto3.resource("s3", region_name=MOTO_MOCK_REGION)
    bucket_name = "test_bucket"
    s3_key = "fruits.csv"
    bucket = conn.create_bucket(Bucket=bucket_name)
    data = build_bytes_io_contents("abc")
    s3_manager = S3DataManager(client=conn, bucket_name=bucket_name)

    metadata = {
        "metadata_field": "metadata_field_value",
        "second_metadata_field": "metadata_field_second_value",
    }

    s3_manager.write_csv(data=data, s3_key=s3_key, metadata=metadata)

    actual_metadata = bucket.Object(s3_key).get()["Metadata"]

    assert actual_metadata == metadata
