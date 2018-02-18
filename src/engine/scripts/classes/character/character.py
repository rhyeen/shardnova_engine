""" Container for <I> Character
"""
from abc import ABC, abstractmethod
from scripts.classes.bank import Bank
from scripts.classes.faction_reputs import FactionReputs
from scripts.classes.drone_warehouse import DroneWarehouse


class Character(ABC):

    def __init__(self, data_handler):
        self.__data_handler = data_handler
        self.__bank = Bank()
        self.__faction_reputs = FactionReputs()
        self.drone_warehouse = DroneWarehouse(self.__data_handler)

    def load_file(self, game_file, universe):
        self._load_file_generics(game_file, universe)
        self._load_file_specifics(game_file)

    def _load_file_generics(self, game_file, universe):
        self.__bank.load_file(game_file['bank'])
        self.__faction_reputs.load_file(game_file['factionReputs'])
        self.drone_warehouse.load_file(game_file['droneWarehouse'], universe)

    @abstractmethod
    def _load_file_specifics(self, game_file):
        raise NotImplementedError

    def get_bank(self):
        return self.__bank

    def get_faction_reputs(self):
        return self.__faction_reputs

    def get_primary_drone(self):
        active_drones = self.drone_warehouse.get_active_drones()
        if len(active_drones) == 0:
            return None
        return active_drones[0]

    def tick(self):
        for drone in self.drone_warehouse.get_active_drones():
            drone.tick()
