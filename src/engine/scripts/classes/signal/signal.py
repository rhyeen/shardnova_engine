""" Container for Signal
"""
from abc import ABC, abstractmethod


class Signal(ABC):

    def __init__(self, data_handler, drone):
        self.__drone = drone
        self.__data_handler = data_handler
        if self.__drone is not None:
            self.galaxy = self.__drone.coordinates.galaxy
            self.sector = self.__drone.coordinates.sector
            self.system = self.__drone.coordinates.system
        self.dropped = False
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

    def set_id(self, forced_id):
        """ Do not use unless expecting to create a mock signal;
            otherwise, you could have two signals with the same id.
        """
        self.__id = forced_id

    @abstractmethod
    def drop(self):
        self.droppped = True
