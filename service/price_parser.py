from bs4 import BeautifulSoup

from service.errors import PriceParserErrors


class PriceParser:
    """Nac Bank currency price parser"""

    def __init__(self, page_content: str) -> None:
        self.page_content = page_content
        self.parser = BeautifulSoup(self.page_content, 'html.parser')

    def get_currency_price(self, currency_code: str) -> str:
        """Returns price of currency by currency_code (for example USD)"""
        try:
            amount, price = self._parse_currency_data(currency_code)
            return self._correct_price(amount, price)
        except AttributeError as error:
            raise PriceParserErrors(f'Failed to parse page content.\n{error}')

    def _parse_currency_data(self, currency_code: str) -> tuple[str, ...]:
        """Extracts amount and amount's price for currency
        by currency_code (for example USD)"""
        rows = self._parse_exchange_rows()
        for code, amount, price in map(self._parse_price_data, rows):
            if code == currency_code:
                return amount, price

    def _parse_exchange_rows(self) -> list[BeautifulSoup]:
        """Extracts rows list from currency exchange table"""
        table = self._parse_exchange_table()
        return table.tbody('tr')

    def _parse_exchange_table(self) -> BeautifulSoup:
        """Extracts currency exchange table from Nac Bank page content"""
        return self.parser.find('table', id='exchangeRates')

    @staticmethod
    def _parse_price_data(row: BeautifulSoup) -> tuple[str, ...]:
        """Extracts currency code, amount and amount's price
        from currency exchange table row"""
        code = row.find(
            attrs={'data-label': "Код літерний"}
        ).text
        amount = row.find(
            attrs={'data-label': "Кількість одиниць валюти"}
        ).text
        price = row.find(
            attrs={'data-label': "Офіційний курс"}
        ).text
        return code, amount, price

    @staticmethod
    def _correct_price(amount: str, price: str) -> str:
        """Returns price for one unit in case if parsed amount not 1"""
        try:
            if amount != 1:
                price = float(price.replace(',', '.')) / int(amount)
            return str(price)
        except ValueError as error:
            raise PriceParserErrors(f'Incorrect price format.\n{error}')
