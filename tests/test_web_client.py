from unittest.mock import patch

from service.web_client import WebClient


@patch('requests.request')
def test_get_page_success(mock_request):

    with open('mockdata/web_client_test_page.html', 'r') as file:
        test_page = file.read()

    mock_request.return_value.text = test_page

    url = "https://example.com/page"
    client = WebClient(url)
    page = client.get_page()

    assert page == test_page
