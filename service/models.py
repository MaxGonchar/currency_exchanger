import datetime
from pprint import pprint

from marshmallow import Schema, fields, post_load


class DayPrice:

    def __init__(self, date, price):
        self.date = date
        self.price = price


class DayPriseSchema(Schema):
    date = fields.Date()
    price = fields.Float()

    @post_load
    def make_object(self, data, **kwargs):
        return DayPrice(**data)


class PriceHistory:

    def __init__(self, price_history: list):
        self.price_history = price_history

    def __iter__(self):
        return iter(self.price_history)


class PriceHistorySchema(Schema):
    price_history = fields.List(fields.Nested(DayPriseSchema))

    @post_load
    def make_object(self, data, **kwargs):
        return PriceHistory(**data)


class Currency:

    def __init__(self, currency_code: str, price_history: PriceHistory):
        self.currency_code = currency_code
        self.price_history = price_history


class CurrencySchema(Schema):
    currency_code = fields.Str()
    price_history = fields.List(fields.Nested(DayPriseSchema))
    # price_history = fields.Nested(PriceHistorySchema)

    @post_load
    def make_object(self, data, **kwargs):
        return Currency(**data)


class Bank:

    def __init__(self, name: str, currencies: list):
        self.name = name
        self.currencies = currencies


class BankSchema(Schema):
    name = fields.Str()
    currencies = fields.List(fields.Nested(CurrencySchema))

    @post_load
    def make_object(self, data, **kwargs):
        return Bank(**data)


if __name__ == '__main__':
    day_price1 = DayPrice(date=datetime.date(202, 10, 23),  price=1.345)
    day_price2 = DayPrice(date=datetime.date(202, 10, 24),  price=1.535)
    day_price3 = DayPrice(date=datetime.date(202, 10, 25),  price=1.125)

    prices = [day_price1, day_price2, day_price3]

    day_price_schema = DayPriseSchema()
    res1 = day_price_schema.dump(day_price1)
    # print(type(res1), res1)
    day_price_obj = day_price_schema.load(res1)
    # print(day_price_obj)
    # print(day_price_obj.__dict__)
    # print('=' * 100)

    price_history = PriceHistory(prices)
    # print('price_history attrs -', price_history.__dict__)
    price_history_schema = PriceHistorySchema()
    res2 = price_history_schema.dump(price_history)
    # print(f'{res2=}')
    price_history_obj = price_history_schema.load(res2)
    # print(f'{price_history_obj=}')
    # print('price_history attrs -', price_history_obj.__dict__)
    # for item in price_history_obj.price_history:
    #     print(item.__dict__)
    # print('=' * 100)

    currency = Currency('USD', price_history)
    currency_schema = CurrencySchema()
    res3 = currency_schema.dump(currency)
    # pprint(res3, indent=2)
    currency_obj = currency_schema.load(res3)
    # print(f'{currency_obj=}')
    # print(currency_obj.__dict__)
    # print('=' * 100)

    bank = Bank('Privat', [currency])
    bank_schema = BankSchema()
    res4 = bank_schema.dump(bank)
    pprint(res4, indent=2)
    bank_obj = bank_schema.load(res4)
    print(f'{bank_obj=}')
    print(bank_obj.currencies)

