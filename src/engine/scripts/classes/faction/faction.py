""" Container for <I> Faction
"""
from abc import ABC, abstractmethod


class Faction(ABC):

    def __init__(self, name):
        self.__name = name

    def __str__(self):
        return 'Faction: {0}'.format(self.get_name())

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
