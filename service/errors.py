class CurrencyExchangerErrors(Exception):

    def __init__(self, message="OOPS"):
        self.message = message

    def logg(self):
        print('*' * 100)
        print(self.message)
        print('*' * 100)


class WebClientError(CurrencyExchangerErrors):

    def __init__(self, message):
        super().__init__(message)
