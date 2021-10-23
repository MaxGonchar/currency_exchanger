import requests


class WebClient:
    """Main web requests client"""

    def __init__(self, url: str):
        self.url = url

    def get_page(self) -> str:
        response = self._request('get')
        page = response.text
        return page

    def _request(self, method: str) -> requests.Response:
        response = requests.request(method, self.url)
        return response
