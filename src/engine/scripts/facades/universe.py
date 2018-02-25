""" Container for Universe
"""
import random
from scripts.classes.galaxy import Galaxy


class Universe(object):

    initial_galaxies = 8

    def __init__(self, data_handler):
        self.__galaxies = []
        self.__starting_galaxy = None
        self.__starting_sector = None
        self.__starting_system = None
        self.__data_handler = data_handler

    def get_galaxies(self):
        return self.__galaxies

    def get_galaxy(self, name):
        if not self.__galaxy_name_exists(name):
            if self.__starting_galaxy.get_name() == name:
                return self.__starting_galaxy
            raise ValueError('{0} is not found.'.format(name))
        index = self.__get_galaxy_index_named(name)
        return self.__get_galaxy(index)

    def __get_galaxy(self, galaxy_index):
        return self.__galaxies[galaxy_index]

    def add_galaxy(self, galaxy):
        if self.__galaxy_exists(galaxy):
            return
        self.__add_galaxy(galaxy)

    def __galaxy_exists(self, galaxy):
        return self.__get_galaxy_index(galaxy) is not None

    def __get_galaxy_index(self, galaxy):
        return self.__get_galaxy_index_named(galaxy.get_name())

    def __galaxy_name_exists(self, galaxy_name):
        return self.__get_galaxy_index_named(galaxy_name) is not None

    def __get_galaxy_index_named(self, galaxy_name):
        for index, __galaxy in enumerate(self.__galaxies):
            if __galaxy.get_name() == galaxy_name:
                return index
        return None

    def __add_galaxy(self, galaxy):
        self.__galaxies.append(galaxy)

    def remove_galaxy(self, galaxy):
        if not self.__galaxy_exists(galaxy):
            raise ValueError('{0} is not found.'.format(galaxy))
        index = self.__get_galaxy_index(galaxy)
        self.__remove_galaxy(index)

    def __remove_galaxy(self, galaxy_index):
        del self.__galaxies[galaxy_index]

    def generate(self):
        for _ in range(self.initial_galaxies):
            galaxy = Galaxy(self.__data_handler)
            galaxy.generate()
            self.add_galaxy(galaxy)
        self.__starting_galaxy = Galaxy(self.__data_handler)
        self.__starting_galaxy.set_as_tutorial()
        self.__starting_sector = self.__starting_galaxy.get_sectors()[0]
        self.__starting_system = self.__starting_sector.get_systems()[0]

    @staticmethod
    def get_random_index(self, given_array):
        return random.randint(0, len(given_array) - 1)

    def get_starting_galaxy(self):
        return self.__starting_galaxy

    def get_starting_sector(self):
        return self.__starting_sector

    def get_starting_system(self):
        return self.__starting_system

    def load_file(self, game_file):
        for galaxy_file in game_file['galaxies']:
            galaxy = Galaxy(self.__data_handler)
            galaxy.load_file(galaxy_file)
            self.add_galaxy(galaxy)
        self.__starting_galaxy = Galaxy(self.__data_handler)
        self.__starting_galaxy.load_file(game_file['startingGalaxy'])
        self.__starting_sector = self.__starting_galaxy.get_sectors()[0]
        self.__starting_system = self.__starting_sector.get_systems()[0]
