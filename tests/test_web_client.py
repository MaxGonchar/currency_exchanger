from unittest.mock import patch

import pytest
import requests

from service.web_client import WebClient
from service.errors import WebClientError


@patch('requests.request')
def test_get_page_success(mock_request):

    with open('mockdata/web_client_test_page.html', 'r') as file:
        test_page = file.read()

    mock_request.return_value.text = test_page

    url = "https://example.com/page"
    client = WebClient(url)
    page = client.get_page()

    assert page == test_page


@patch('requests.request')
def test_request_http_error(mock_request):
    mock_request.side_effect = requests.exceptions.HTTPError('Some HTTP Error')
    url = "https://example.com/page"
    client = WebClient(url)

    with pytest.raises(WebClientError) as error:
        client.get_page()

    assert str(error.value.message) == 'Some HTTP Error'
    assert error.value.reason == 'WebClient error'

