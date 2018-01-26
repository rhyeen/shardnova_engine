""" Container for PhoneBook
"""


class PhoneBook(object):

    def __init__(self):
        self.__phones = self.__get_phones_config()

    @staticmethod
    def __get_phones_config():
        return {
            'primary': None,
            'secondary': None,
            'other': []
        }

    def get_primary_phone_number(self):
        return self.__phones['primary']

    def get_secondary_phone_number(self):
        return self.__phones['secondary']

    def get_other_phone_numbers(self):
        return self.__phones['other']

    def set_primary_phone_number(self, phone):
        self.__phones['primary'] = phone

    def set_secondary_phone_number(self, phone):
        self.__phones['secondary'] = phone

    def add_other_phone_number(self, phone):
        self.__phones['other'].append(phone)

    def clear_other_phone_numbers(self):
        self.__phones['other'] = []

    def set_other_phone_numbers(self, phones):
        self.__phones['other'] = phones

    def reset_phone_book(self):
        self.__phones = self.__get_phones_config()
