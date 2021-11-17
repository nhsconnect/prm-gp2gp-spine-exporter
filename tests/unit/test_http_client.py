from unittest.mock import MagicMock

import pytest

from prmexporter.http_client import HttpClient, HttpClientException


def _build_mock_response(content=None, status_code=200):
    mock_response = MagicMock()
    mock_response.content = content
    mock_response.status_code = status_code
    return mock_response


def test_makes_an_api_call_to_given_url_with_auth_token_and_returns_data():
    mock_client = MagicMock()
    test_url = "https://test.com"
    test_token = "Abc123"
    mock_response = _build_mock_response(
        content=b'{"data": [{"fruit": "mango", "colour": "orange"}]}'
    )

    mock_client.get.side_effect = [mock_response]

    http_client = HttpClient(url=test_url, client=mock_client)

    expected_header = {"Accept": "application/json", "Authorization": f"Bearer {test_token}"}
    expected_data = {"data": [{"fruit": "mango", "colour": "orange"}]}

    actual_data = http_client.fetch_data(test_token)

    mock_client.get.assert_called_with(url=test_url, headers=expected_header)
    assert actual_data == expected_data


def test_throws_exception_when_status_code_is_not_200():
    mock_client = MagicMock()
    test_token = "Abc123"
    mock_response = _build_mock_response(status_code=500)

    mock_client.get.side_effect = [mock_response]

    http_client = HttpClient(url="test.com", client=mock_client)

    with pytest.raises(HttpClientException) as e:
        http_client.fetch_data(test_token)

    assert str(e.value) == "Unable to fetch data from test.com with status code: 500"
