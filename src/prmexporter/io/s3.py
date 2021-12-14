import logging
from io import BytesIO

logger = logging.getLogger(__name__)


class S3DataManager:
    def __init__(self, client, bucket_name: str):
        self._client = client
        self._bucket_name = bucket_name
        self._s3_spine_output_data_bucket = self._client.Bucket(self._bucket_name)

    def write_csv(self, data: BytesIO, s3_key: str):
        object_uri = f"s3://{self._bucket_name}/{s3_key}"
        logger.info(
            "Attempting to upload to S3",
            extra={"event": "ATTEMPTING_UPLOAD_CSV_TO_S3", "object_uri": object_uri},
        )

        self._s3_spine_output_data_bucket.upload_fileobj(data, s3_key)

        logger.info(
            "Successfully uploaded to S3",
            extra={"event": "UPLOADED_CSV_TO_S3", "object_uri": object_uri},
        )
