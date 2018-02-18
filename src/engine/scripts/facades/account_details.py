""" Container for AccountDetails
"""
from scripts.classes.phone_book import PhoneBook
from scripts.classes.patreon_details import PatreonDetails
from scripts.classes.sms_credits import SmsCredits


class AccountDetails(object):

    def __init__(self):
        self.__phone_book = PhoneBook()
        self.__patreon_details = PatreonDetails()
        self.__sms_credits = SmsCredits()

    def get_phone_book(self):
        return self.__phone_book

    def set_phone_book(self, phone_book):
        self.__phone_book = phone_book

    def get_patreon_details(self):
        return self.__patreon_details

    def set_patreon_details(self, patreon_details):
        self.__patreon_details = patreon_details

    def get_sms_credits(self):
        return self.__sms_credits

    def set_sms_credits(self, sms_credits):
        self.__sms_creditss = sms_credits

    def get_remaining_sms_credits(self):
        return self.__sms_credits.get_remaining_credits()

    def get_primary_phone_number(self):
        return self.__phone_book.get_primary_phone_number()
