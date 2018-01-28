""" Container for Interactor
"""
from scripts.facades.user import User


class Interactor(object):

    def __init__(self, data_handler, output_handler, game):
        """ game must come preloaded
        """
        self.__data_handler = data_handler
        self.__output_handler = output_handler
        self.__game = game

    def initialize_game(self):
        self.__game.initialize_game()

    def create_phone_user(self, phone):
        user = User(self.__data_handler)
        user.set_primary_phone(phone)
        is_new_user = self.__game.new_user(user)
        if is_new_user:
            self.__output_handler.send_welcome_message(user)

    def set_course(self, drone, destination_celestial_body):
        drone.coordinates.set_course(destination_celestial_body)
