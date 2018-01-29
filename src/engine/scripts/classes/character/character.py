""" Container for <I> Character
"""
from abc import ABC
from scripts.classes.bank import Bank
from scripts.classes.faction_reputs import FactionReputs
from scripts.classes.drone_warehouse import DroneWarehouse


class Character(ABC):

    def __init__(self):
        self.__bank = Bank()
        self.__faction_reputs = FactionReputs()
        self.drone_warehouse = DroneWarehouse()

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
        for drone in self.get_active_drones():
            drone.tick()
