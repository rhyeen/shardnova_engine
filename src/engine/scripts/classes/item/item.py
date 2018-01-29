""" Container for Item
"""
from abc import ABC, abstractmethod


class Item(ABC):

    @abstractmethod
    def modifies_fuel(self):
        return False

    @abstractmethod
    def modifies_distance_per_tick(self):
        return 0

    @abstractmethod
    def modifies_fuel_per_distance(self):
        return 0
