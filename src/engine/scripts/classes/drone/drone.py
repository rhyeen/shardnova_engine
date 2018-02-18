""" Container for <I> Drone
"""
from abc import ABC, abstractmethod
from scripts.classes.coordinates import Coordinates


class Drone(ABC):

    def __init__(self, data_handler):
        self.__data_handler = data_handler
        self.__id = self.__get_unique_id()
        self.__inventory = self._get_default_inventory()
        self.coordinates = Coordinates()
        self.fuel = 0

    def __str__(self):
        return 'Drone: {0}'.format(self.get_id())

    def __get_unique_id(self):
        return self.__data_handler.get_unique_id('drone')

    @staticmethod
    @abstractmethod
    def _get_default_inventory():
        return None

    def get_id(self):
        return self.__id

    def get_inventory(self):
        return self.__inventory

    def tick(self):
        self.coordinates.tick()
        if self.coordinates.on_course():
            self.__use_fuel()

    def __use_fuel(self):
        self.fuel -= self.__get_fuel_per_tick()
        if self.fuel >= 0:
            return
        self.fuel = 0
        if not self.coordinates.on_course():
            return
        self.coordinates.get_course().pause_course()

    def get_distance_per_tick(self):
        items = self.get_inventory().get_all_items()
        modification = 1
        for item in items:
            if item.modifies_distance_per_tick():
                modification += item.modifies_distance_per_tick()
        return self.get_default_distance_per_tick() * modification

    @abstractmethod
    def get_default_distance_per_tick(self):
        return 1

    def get_fuel_per_distance(self):
        items = self.get_inventory().get_all_items()
        modification = 1
        for item in items:
            if item.modifies_fuel_per_distance():
                modification += item.modifies_fuel_per_distance()
        return self.get_default_fuel_per_distance() * modification

    def __get_fuel_per_tick(self):
        return self.get_distance_per_tick() * self.get_fuel_per_distance()

    @abstractmethod
    def get_default_fuel_per_distance(self):
        return 1
