""" Container for <I> Bank
"""


class Bank(object):

    def __init__(self):
        self.__black_market_account = None
        self.__universal_federation_account = None
        self.__primary_account = self.__get_default_primary_account()

    @staticmethod
    def __get_default_primary_account():
        return 'ufa'

    def get_black_market_account(self):
        return self.__black_market_account

    def set_black_market_account(self, bank_account):
        self.__black_market_account = bank_account

    def get_universal_federation_account(self):
        return self.__universal_federation_account

    def set_universal_federation_account(self, bank_account):
        self.__universal_federation_account = bank_account

    def get_primary_account(self):
        if (self.__primary_account == 'ufa'):
            return self.__universal_federation_account
        return self.__black_market_account

    def set_black_market_as_primary_account(self):
        self.__primary_account = 'bm'

    def set_universal_federation_account_as_primary_account(self):
        self.__primary_account = 'ufa'
