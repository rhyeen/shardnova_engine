""" Container for Universe
"""


class Universe(object):

    def __init__(self):
        self.__galaxies = []

    def get_galaxies(self):
        return self.__galaxies

    def add_galaxy(self, galaxy):
        if self.__galaxy_exists(galaxy):
            return
        self.__add_galaxy(galaxy)

    def __galaxy_exists(self, galaxy):
        return self.__get_galaxy_index(galaxy) is not None

    def __get_galaxy_index(self, galaxy):
        for index, __galaxy in enumerate(self.__galaxies):
            if (__galaxy.get_name() == galaxy.get_name()):
                return index
        return None

    def __add_galaxy(self, galaxy):
        self.__galaxies.append(galaxy)

    def remove_galaxy(self, galaxy):
        if not self.__galaxy_exists(galaxy):
            raise ValueError('{0} is not found.'.format(galaxy))
        index = self.__get_galaxy_index(galaxy)
        self.__remove_galaxy(self, index)

    def __remove_galaxy(self, galaxy_index):
        del self.__galaxies[galaxy_index]
