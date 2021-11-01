import pytest
from bs4 import BeautifulSoup

from service.price_parser import PriceParser
from service.errors import PriceParserErrors


def set_prise(page_content: str, price: str):
    parser = BeautifulSoup(page_content, 'html.parser')
    for row in parser.find('table', id='exchangeRates').tbody('tr'):
        if row.find(attrs={'data-label': "Код літерний"}).text == 'USD':
            row.find(attrs={'data-label': "Офіційний курс"}).string = price
    return str(parser)


def test_get_currency_price_success():
    with open('mockdata/nac_bank_test_page.html', 'r') as file:
        test_page = file.read()

    price_parser = PriceParser(test_page)

    assert price_parser.get_currency_price('USD') == '26.349'


def test_get_currency_prise_bad_html():
    test_page = "<h1>BAD HTML</h1>"
    price_parser = PriceParser(test_page)

    with pytest.raises(PriceParserErrors) as error:
        price_parser.get_currency_price('USD')

    assert error.value.message == "Failed to parse page content.\n" \
                                  "'NoneType' object has no attribute 'tbody'"
    assert error.value.reason == 'PriceParser error'


def test_get_currency_prise_bad_price_format():
    with open('mockdata/nac_bank_test_page.html', 'r') as file:
        test_page = file.read()

    test_page = set_prise(test_page, '1,2,3')
    price_parser = PriceParser(test_page)

    with pytest.raises(PriceParserErrors) as error:
        price_parser.get_currency_price('USD')

    assert error.value.message == "Incorrect price format.\n" \
                                  "could not convert string to float: '1.2.3'"
    assert error.value.reason == 'PriceParser error'
