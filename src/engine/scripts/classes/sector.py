""" Container for Sector
"""


class Sector(object):

    def __init__(self, name=None):
        self.__systems = []
        if name is None:
            name = self.__get_unique_name()
        self.__name = name

    def __str__(self):
        return 'Sector: {0}'.format(self.get_name())

    def __get_unique_name(self):
        return self.__data_handler.get_unique_name('sector')

    def get_name(self):
        return self.__name

    def get_systems(self):
        return self.__systems

    def add_system(self, system):
        if self.__system_exists(system):
            return
        self.__add_system(system)

    def __system_exists(self, system):
        return self.__get_system_index(system) is not None

    def __get_system_index(self, system):
        for index, __system in enumerate(self.__systems):
            if (__system.get_name() == system.get_name()):
                return index
        return None

    def __add_system(self, system):
        self.__systems.append(system)

    def remove_system(self, system):
        if not self.__system_exists(system):
            raise ValueError('{0} is not found.'.format(system))
        index = self.__get_system_index(system)
        self.__remove_system(self, index)

    def __remove_system(self, system_index):
        del self.__systems[system_index]
