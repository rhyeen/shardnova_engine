""" Container for Galaxy
"""
import random
from scripts.classes.sector import Sector


class Galaxy(object):

    max_sectors = 8

    def __init__(self, data_handler, name=None):
        self.__sectors = []
        self.__data_handler = data_handler
        if name is None:
            name = self.__get_unique_name()
        self.__name = name

    def __str__(self):
        return 'Galaxy: {0}'.format(self.get_name())

    def __get_unique_name(self):
        return self.__data_handler.get_unique_name('galaxy')

    def get_name(self):
        return self.__name

    def get_sectors(self):
        return self.__sectors

    def add_sector(self, sector):
        if self.__sector_exists(sector):
            return
        self.__add_sector(sector)

    def __sector_exists(self, sector):
        return self.__get_sector_index(sector) is not None

    def __get_sector_index(self, sector):
        for index, __sector in enumerate(self.__sectors):
            if (__sector.get_name() == sector.get_name()):
                return index
        return None

    def __add_sector(self, sector):
        self.__sectors.append(sector)

    def remove_sector(self, sector):
        if not self.__sector_exists(sector):
            raise ValueError('{0} is not found.'.format(sector))
        index = self.__get_sector_index(sector)
        self.__remove_sector(self, index)

    def __remove_sector(self, sector_index):
        del self.__sectors[sector_index]

    def generate(self):
        total = random.randint(1, self.max_sectors)
        for _ in range(total):
            sector = Sector(self.__data_handler)
            sector.generate()
            self.add_sector(sector)

    def set_as_tutorial(self):
        self.__sectors = []
        sector = Sector(self.__data_handler)
        sector.set_as_tutorial()
        self.add_sector(sector)
