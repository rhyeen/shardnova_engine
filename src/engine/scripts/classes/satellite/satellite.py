""" Container for <I> Satellite
"""
from abc import ABC, abstractmethod


class Satellite(ABC):

    def __init__(self, data_handler):
        self.__data_handler = data_handler
        self.__name = self.__get_unique_name()

    def __str__(self):
        return 'Satellite: {0}'.format(self.get_name())

    def __get_unique_name(self):
        return self.__data_handler.get_unique_name('satellite')

    def get_name(self):
        return self.__name

    def load_file(self, game_file):
        self._load_file_generics(game_file)
        self._load_file_specifics(game_file)

    def _load_file_generics(self, game_file):
        self.__name = game_file['name']

    @abstractmethod
    def _load_file_specifics(self, game_file):
        raise NotImplementedError
