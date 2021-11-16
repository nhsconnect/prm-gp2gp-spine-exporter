from unittest.mock import MagicMock

from prmexporter.domain.http_client import HttpClient


def _build_mock_response(content=None, status_code=200):
    mock_response = MagicMock()
    mock_response.content = content
    mock_response.status_code = status_code
    return mock_response


def test_makes_an_api_call_to_given_url_and_returns_response():
    mock_client = MagicMock()
    test_url = "https://test.com"
    mock_response = _build_mock_response(
        content=b'{"data": [{"fruit": "mango", "colour": "orange"}]}'
    )

    mock_client.get.side_effect = [mock_response]

    client = HttpClient(url=test_url, client=mock_client)

    expected = {"data": [{"fruit": "mango", "colour": "orange"}]}

    actual = client.fetch_data()

    mock_client.get.assert_called_with(test_url)
    assert actual == expected
