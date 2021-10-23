from service.price_parser import PriceParser


def test_get_currency_price():
    with open('mockdata/nac_bank_test_page.html', 'r') as file:
        test_page = file.read()

    price_parser = PriceParser(test_page)
    assert price_parser.get_currency_price('USD') == '26.349'
