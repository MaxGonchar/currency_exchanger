from datetime import date

from service.web_client import WebClient
from service.price_parser import PriceParser

day = date.today().strftime('%d.%m.%Y')
url = f'https://bank.gov.ua/ua/markets/exchangerates?date={day}&period=daily'
client = WebClient(url)
price_parser = PriceParser(client.get_page())
price = price_parser.get_currency_price('USD')
print(price)
