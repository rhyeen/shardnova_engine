""" Container for <I> Drone
"""
from abc import ABC, abstractmethod
from scripts.classes.coordinates import Coordinates


class Drone(ABC):

    def __init__(self, data_handler):
        self.__data_handler = data_handler
        self.__id = self.__get_unique_id()
        self.__inventory = self._get_default_inventory()
        self.coordinates = Coordinates()

    def __str__(self):
        return 'Drone: {0}'.format(self.get_id())

    def __get_unique_id(self):
        return self.__data_handler.get_unique_id('drone')

    @staticmethod
    @abstractmethod
    def _get_default_inventory():
        return None

    def get_id(self):
        return self.__id

    def get_inventory(self):
        return self.__inventory

    def tick(self):
        self.coordinates.tick()
