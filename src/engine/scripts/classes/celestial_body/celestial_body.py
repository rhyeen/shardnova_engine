""" Container for <I> CelestialBody
"""
from abc import ABC, abstractmethod
from scripts.classes.satellite.hyperspace_gate import HyperspaceGate
from scripts.classes.satellite.moon import Moon
from scripts.classes.satellite.station import Station


class CelestialBody(ABC):

    def __init__(self, data_handler, name=None):
        self._data_handler = data_handler
        self._satellites = []
        if name is None:
            name = self._get_unique_name()
        self._name = name

    @abstractmethod
    def __str__(self):
        return 'Celestial body: {0}'.format(self.get_name())

    def get_name(self):
        return self._name

    @abstractmethod
    def _get_unique_name(self):
        return self._data_handler.get_unique_name('celestial_body')

    def get_satellites(self):
        return self._satellites

    def add_satellite(self, satellite):
        if self.__satellite_exists(satellite):
            return
        self.__add_satellite(satellite)

    def __satellite_exists(self, satellite):
        return self.__get_satellite_index(satellite) is not None

    def __get_satellite_index(self, satellite):
        for index, _satellite in enumerate(self._satellites):
            if _satellite.get_name() == satellite.get_name():
                return index
        return None

    def __add_satellite(self, satellite):
        self._satellites.append(satellite)

    def remove_satellite(self, satellite):
        if not self.__satellite_exists(satellite):
            raise ValueError('{0} is not found.'.format(satellite))
        index = self.__get_satellite_index(satellite)
        self.__remove_satellite(index)

    def __remove_satellite(self, satellite_index):
        del self._satellites[satellite_index]

    def load_file(self, game_file):
        self._load_file_generics(game_file)
        self._load_file_specifics(game_file)

    def _load_file_generics(self, game_file):
        self._name = game_file['name']
        for satellite_file in game_file['satellites']:
            satellite = self.__load_file_satellite(satellite_file)
            self.add_satellite(satellite)

    def __load_file_satellite(self, game_file):
        satellite_type = game_file['type']
        if satellite_type == 'hyperspaceGate':
            satellite = HyperspaceGate(self._data_handler)
        elif satellite_type == 'moon':
            satellite = Moon(self._data_handler)
        elif satellite_type == 'station':
            satellite = Station(self._data_handler)
        else:
            raise ValueError('Satellite of type "{0}" unsupported'.format(satellite_type))
        satellite.load_file(game_file)
        return satellite

    @abstractmethod
    def _load_file_specifics(self, game_file):
        raise NotImplementedError
