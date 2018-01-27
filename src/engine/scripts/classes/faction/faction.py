""" Container for <I> Faction
"""
from abc import ABC


class Faction(ABC):

    def __init__(self, name):
        self.__name = name

    def __str__(self):
        return 'Faction: {0}'.format(self.get_name())

    def get_name(self):
        return self.__name
