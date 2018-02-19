""" Container for Item
"""
from abc import ABC, abstractmethod


class Item(ABC):

    def __init__(self, durability=None):
        self.max_durability = self._get_max_durability()
        if self.max_durability <= 0:
            raise ValueError('Max durability of an item must be a positive number')
        if durability is None:
            durability = self.max_durability
        self.durability = durability
        self.cost_per_repair_point = self._get_cost_per_repair_point()

    @staticmethod
    @abstractmethod
    def _get_max_durability():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def _get_cost_per_repair_point():
        raise NotImplementedError

    def modifies_distance_per_tick(self):
        return self._alter_by_durability(0)

    def modifies_fuel_per_distance(self):
        return self._alter_by_durability(0)

    def load_file(self, game_file):
        self._load_file_generics(game_file)
        self._load_file_specifics(game_file)

    def _load_file_generics(self, game_file):
        self.durability = game_file['durability']

    @abstractmethod
    def _load_file_specifics(self, game_file):
        raise NotImplementedError

    def _alter_by_durability(self, value):
        return value * (self.durability / self.max_durability)
