""" Container for User
"""
from scripts.facades.account_details import AccountDetails


class User(object):

    def __init__(self):
        self.__account_details = AccountDetails()
