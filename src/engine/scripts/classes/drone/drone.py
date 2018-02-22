""" Container for <I> Drone
"""
from abc import ABC, abstractmethod
from scripts.classes.coordinates import Coordinates
from scripts.classes.inventory.basic_inventory import BasicInventory


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

    def tick(self, output_handler):
        distance_traveled, course = self.coordinates.tick()
        if distance_traveled > 0:
            self.__use_fuel(distance_traveled)
        if course and course.is_finished():
            output_handler.reached_destination(self, course)

    def __use_fuel(self, distance_traveled):
        self.fuel -= self.get_fuel_per_distance() * distance_traveled
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

    @abstractmethod
    def get_default_fuel_per_distance(self):
        return 1

    def load_file(self, game_file, universe):
        self._load_file_generics(game_file, universe)
        self._load_file_specifics(game_file)

    def _load_file_generics(self, game_file, universe):
        self.__id = game_file['id']
        self.fuel = game_file['fuel']
        self.load_file_inventory(game_file['inventory'])
        self.coordinates.load_file(game_file['coordinates'], universe, self)

    def load_file_inventory(self, game_file):
        inventory_type = game_file['type']
        if inventory_type == 'basic':
            self.__inventory = BasicInventory()
        else:
            raise ValueError('Inventory of type "{0}" unsupported'.format(inventory_type))
        self.__inventory.load_file(game_file)

    @abstractmethod
    def _load_file_specifics(self, game_file):
        raise NotImplementedError
