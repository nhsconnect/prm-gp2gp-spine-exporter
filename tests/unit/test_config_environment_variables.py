import pytest

from prmexporter.config import MissingEnvironmentVariable, SpineExporterConfig


def test_reads_from_environment_variables():
    environment = {
        "SPLUNK_URL": "https://test.com",
        "SPLUNK_API_TOKEN_PARAM_NAME": "/param/name/api-token",
        "OUTPUT_SPINE_DATA_BUCKET": "output-spine-data-bucket",
        "BUILD_TAG": "61ad1e1c",
        "S3_ENDPOINT_URL": "https://an.endpoint:3000",
    }

    expected_config = SpineExporterConfig(
        splunk_url="https://test.com",
        splunk_api_token_param_name="/param/name/api-token",
        output_spine_data_bucket="output-spine-data-bucket",
        build_tag="61ad1e1c",
        s3_endpoint_url="https://an.endpoint:3000",
    )

    actual_config = SpineExporterConfig.from_environment_variables(environment)

    assert actual_config == expected_config


def test_error_from_environment_when_required_fields_are_not_set():
    environment = {"SPLUNK_API_TOKEN_PARAM_NAME": "/param/name/api-token"}

    with pytest.raises(MissingEnvironmentVariable) as e:
        SpineExporterConfig.from_environment_variables(environment)

    assert str(e.value) == "Expected environment variable SPLUNK_URL was not set, exiting..."


def test_reads_from_environment_variables_when_optional_fields_are_not_set():
    environment = {
        "SPLUNK_URL": "https://test.com",
        "SPLUNK_API_TOKEN_PARAM_NAME": "/param/name/api-token",
        "OUTPUT_SPINE_DATA_BUCKET": "output-spine-data-bucket",
        "BUILD_TAG": "61ad1e1c",
    }

    expected_config = SpineExporterConfig(
        splunk_url="https://test.com",
        splunk_api_token_param_name="/param/name/api-token",
        output_spine_data_bucket="output-spine-data-bucket",
        build_tag="61ad1e1c",
        s3_endpoint_url=None,
    )

    actual_config = SpineExporterConfig.from_environment_variables(environment)

    assert actual_config == expected_config