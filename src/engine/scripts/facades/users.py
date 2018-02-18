""" Container for Users
"""
from scripts.facades.user import User


class Users(object):

    def __init__(self, data_handler):
        self.__data_handler = data_handler
        self.__users = []

    def get_users(self):
        return self.__users

    def add_user(self, user):
        if self.__user_exists(user):
            return False
        self.__add_user(user)
        return True

    def __user_exists(self, user):
        return self.__get_user_index(user) is not None

    def __get_user_index(self, user):
        for index, __user in enumerate(self.__users):
            if (__user.shares_identifiers(user)):
                return index
        return None

    def __add_user(self, user):
        self.__users.append(user)

    def remove_user(self, user):
        if not self.__user_exists(user):
            raise ValueError('{0} is not found.'.format(user))
        index = self.__get_user_index(user)
        self.__remove_user(self, index)

    def __remove_user(self, user_index):
        del self.__users[user_index]

    def tick(self):
        for user in self.__users:
            user.tick()

    def load_file(self, game_file, universe):
        for user_file in game_file:
            user = User(self.__data_handler, None)
            user.load_file(user_file, universe)
            self.add_user(user)
