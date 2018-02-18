""" Container for User
"""
from scripts.facades.account_details import AccountDetails
from scripts.classes.character.player_character import PlayerCharacter
from scripts.interfaces.output_handler.console_output_handler import ConsoleOutputHandler


class User(object):

    def __init__(self, data_handler, output_handler, user_id=None):
        self.__data_handler = data_handler
        self.output_handler = output_handler
        self.__account_details = AccountDetails()
        self.character = PlayerCharacter(self.__data_handler)
        if user_id is None:
            user_id = self.__get_unique_id()
        self.__id = user_id

    def __str__(self):
        return 'User: {0}'.format(self.get_id())

    def get_id(self):
        return self.__id

    def __get_unique_id(self):
        return self.__data_handler.get_unique_id('user')

    def shares_identifiers(self, user):
        if self.get_id() == user.get_id():
            return True
        if self.__has_any_phone(user.get_phone_book().get_all_phones()):
            return True
        if self.__has_patreon_id(user.get_account_details().get_patreon_id()):
            return True
        return False

    def __has_any_phone(self, phones):
        return self.get_phone_book().has_any_phone(phones)

    def __has_patreon_id(self, patreon_id):
        return self.get_patreon_details().get_patreon_id() == patreon_id

    def get_account_details(self):
        return self.__account_details

    def get_phone_book(self):
        return self.__account_details.get_phone_book()

    def get_patreon_details(self):
        return self.__account_details.get_patreon_details()

    def set_primary_phone(self, phone):
        self.get_phone_book().set_primary_phone_number(phone)

    def get_primary_phone(self):
        return self.get_phone_book().get_primary_phone_number()

    def tick(self):
        self.character.tick()

    def load_file(self, game_file, universe):
        self.__load_output_handler(game_file)
        self.__id = game_file['id']
        self.__account_details.load_file(game_file['accountDetails'])
        self.character.load_file(game_file['character'], universe)

    def __load_output_hanlder(self, game_file):
        output_handler_type = game_file['outputHandler']
        if output_handler_type == 'console':
            self.output_handler = ConsoleOutputHandler()
        else:
            raise ValueError('Output handler of type "{0}" unsupported'.format(output_handler_type))
