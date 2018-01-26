""" Container for <I> Drone
"""
from abc import ABC, abstractmethod


class Drone(ABC):

    def __init__(self, data_handler):
        self.__data_handler = data_handler
        self.__id = self.__get_unique_id()
        self.__inventory = self._get_default_inventory()

    def __get_unique_id(self):
        return self.__data_handler.get_unique_id('drone')

    @staticmethod
    @abstractmethod
    def _get_default_inventory():
        return None

    def get_id(self):
        return self.__id
