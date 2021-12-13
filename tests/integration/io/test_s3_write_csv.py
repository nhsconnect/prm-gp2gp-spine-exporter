from io import BytesIO

import boto3
from moto import mock_s3

from prmexporter.io.s3 import S3DataManager
from tests.builders.file import build_csv_contents

MOTO_MOCK_REGION = "us-east-1"


@mock_s3
def test_writes_bytes_as_csv_to_s3_bucket():
    conn = boto3.resource("s3", region_name=MOTO_MOCK_REGION)
    bucket = conn.create_bucket(Bucket="test_bucket")

    csv_data = build_csv_contents(
        header=["header1", "header2"],
        rows=[["row1-col1", "row1-col2"], ["row2-col1", "row2-col2"]],
    )

    bytes_data = str.encode(csv_data)

    s3_manager = S3DataManager(client=conn, bucket_name="test_bucket")
    s3_manager.write_csv(data=BytesIO(bytes_data), s3_key="v3/fruits.csv")

    actual = bucket.Object("v3/fruits.csv").get()["Body"].read()

    assert actual == bytes_data
