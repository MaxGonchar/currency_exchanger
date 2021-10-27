class CurrencyExchangerErrors(Exception):

    def __init__(self, reason='Unknown error', message="OOPS"):
        self.reason = reason
        self.message = message

    def logg(self):
        print('*' * 100)
        print(self.reason)
        print(self.message)
        print('*' * 100)


class WebClientError(CurrencyExchangerErrors):

    def __init__(self, message):
        self.reason = 'WebClient error'
        super().__init__(self.reason, message)


class PriceParserErrors(CurrencyExchangerErrors):

    def __init__(self, message):
        self.reason = 'PriceParser error'
        super().__init__(self.reason, message)
