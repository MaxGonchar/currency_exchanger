import requests


class WebClient:
    """Main web requests client"""

    def __init__(self, url):
        self.url = url

    def get_page(self):
        response = self._request('get')
        page = response.text
        return page

    def _request(self, method):
        response = requests.request(method, self.url)
        return response


if __name__ == '__main__':
    url = 'https://bank.gov.ua/ua/markets/exchangerates?date=14.10.2021&period=daily'
    client = WebClient(url)
    page = client.get_page()
    print(page)
