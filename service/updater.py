from datetime import date

from service.web_client import WebClient
from service.price_parser import PriceParser
from service.errors import CurrencyExchangerErrors


def update_currency_prices():
    day = date.today().strftime('%d.%m.%Y')
    url = f'https://bank.gov.ua/ua/markets/exchangerates?date={day}&period=daily'
    client = WebClient(url)
    price_parser = PriceParser(client.get_page())
    price = price_parser.get_currency_price('USD')
    print(price)


if __name__ == '__main__':
    # update_currency_prices()
    try:
        update_currency_prices()
    except CurrencyExchangerErrors as error:
        error.logg()
