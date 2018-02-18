""" Container for <I> Satellite
"""
from abc import ABC


class Satellite(ABC):

    def __init__(self, data_handler):
        self.__data_handler = data_handler
        self.__id = self.__get_unique_id()

    def __str__(self):
        return 'Satellite: {0}'.format(self.get_id())

    def __get_unique_id(self):
        return self.__data_handler.get_unique_id('satellite')

    def get_id(self):
        return self.__id
