""" Container for <I> CelestialBody
"""
from abc import ABC, abstractmethod


class CelestialBody(ABC):

    def __init__(self, name, data_handler):
        self._data_handler = data_handler
        self.__satellites = []
        if name is None:
            name = self._get_unique_name()
        self.__name = name

    @abstractmethod
    def _get_unique_name(self):
        return self._data_handler.get_unique_name('celestial_body')

    def get_satellites(self):
        return self.__satellites

    def set_satellites(self, satellites):
        self.__satellites = satellites

    def add_satellite(self, satellite):
        if self.__satellite_exists(satellite):
            return
        self.__add_satellite(satellite)

    def __satellite_exists(self, satellite):
        return self.__get_satellite_index(satellite) is not None

    def __get_satellite_index(self, satellite):
        for index, __satellite in enumerate(self.__satellites):
            if (__satellite.get_id() == satellite.get_id()):
                return index
        return None

    def __add_satellite(self, satellite):
        self.__satellites.append(satellite)

    def remove_satellite(self, satellite):
        if not self.__satellite_exists(satellite):
            raise ValueError('{0} is not found.'.format(satellite))
        index = self.__get_satellite_index(satellite)
        self.__remove_satellite(self, index)

    def __remove_satellite(self, satellite_index):
        del self.__satellites[satellite_index]
