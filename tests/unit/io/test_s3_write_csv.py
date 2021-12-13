from unittest.mock import MagicMock

from prmexporter.io.s3 import S3DataManager
from tests.builders.file import build_bytes_io_contents, build_csv_contents

MOTO_MOCK_REGION = "us-east-1"


def test_calls_client_upload_fileobj_with_key_and_data():
    mock_s3_client = MagicMock()
    bucket_name = "test_bucket"
    bucket_mock = MagicMock()
    mock_s3_client.Bucket = MagicMock(return_value=bucket_mock)

    csv_data = build_csv_contents(
        header=["header1", "header2"],
        rows=[["row1-col1", "row1-col2"], ["row2-col1", "row2-col2"]],
    )
    data = build_bytes_io_contents(csv_data)

    s3_manager = S3DataManager(client=mock_s3_client, bucket_name=bucket_name)
    s3_manager.write_csv(data=data, s3_key="v2/fruits.csv")

    mock_s3_client.Bucket.assert_called_once_with(bucket_name)
    bucket_mock.upload_fileobj.assert_called_once_with(data, "v2/fruits.csv")
