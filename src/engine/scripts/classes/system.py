""" Container for System
"""
from scripts.classes.orbital_plane import OrbitalPlane


class System(object):

    def __init__(self, name, data_handler):
        self.__data_handler = data_handler
        self.__orbital_plane = OrbitalPlane()
        if name is None:
            name = self.__get_unique_name()
        self.__name = name

    def __str__(self):
        return 'System: {0}'.format(self.get_name())

    def __get_unique_name(self):
        return self.__data_handler.get_unique_name('system')

    def get_name(self):
        return self.__name

    def get_celestial_bodies(self):
        self.__orbital_plane.get_celestial_bodies()

    def get_distances(self, celestial_body):
        self.__orbital_plane.get_distances(celestial_body)

    def get_distance_between_celestial_bodies(self, body1, body2):
        self.__orbital_plane.get_distance_between_celestial_bodies(body1, body2)
