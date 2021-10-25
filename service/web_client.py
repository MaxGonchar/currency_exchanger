import requests

from service.errors import WebClientError


class WebClient:
    """Main web requests client"""

    def __init__(self, url: str):
        self.url = url

    def get_page(self) -> str:
        try:
            response = self._request('get')
            page = response.text
            return page
        except requests.exceptions.RequestException as error:
            raise WebClientError(error)

    def _request(self, method: str) -> requests.Response:
        response = requests.request(method, self.url)
        response.raise_for_status()
        return response
