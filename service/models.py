import datetime

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


class Currency(Schema):
    ...


class Bank(Schema):
    ...


if __name__ == '__main__':
    day_price = DayPrice(
        date=datetime.date(202, 10, 23),
        price=1.345
    )
    schema = DayPriseSchema()
    res = schema.dump(day_price)
    day_price_2 = schema.load(res)
    print(day_price_2)
    print(day_price_2.date)
    print(day_price_2.price)

