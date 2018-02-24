""" Container for Signal
"""
from abc import ABC, abstractmethod


class Signal(ABC):

    def __init__(self, data_handler, drone):
        self.__drone = drone
        self.__data_handler = data_handler
        self.galaxy = self.__drone.coordinates.galaxy
        self.sector = self.__drone.coordinates.sector
        self.system = self.__drone.coordinates.system
        self.__id = self.__get_unique_id()

    def __str__(self):
        return '{0}: {1}'.format(self.get_signal_type(), self.get_id())

    @staticmethod
    @abstractmethod
    def get_signal_type():
        raise NotImplementedError

    def __get_unique_id(self):
        return self.__data_handler.get_unique_id('signal')

    def get_id(self):
        return self.__id
