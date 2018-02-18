""" Container for <I> BankAccount
"""
from abc import ABC, abstractmethod


class BankAccount(ABC):

    def __init__(self):
        pass

    def load_file(self, game_file):
        self._load_file_generics(game_file)
        self._load_file_specifics(game_file)

    def _load_file_generics(self, game_file):
        pass

    @abstractmethod
    def _load_file_specifics(self, game_file):
        raise NotImplementedError
