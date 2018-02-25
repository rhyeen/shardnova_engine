""" Container for MuleClassTanker
"""
from scripts.classes.drone.drone import Drone
from scripts.classes.inventory.basic_inventory import BasicInventory


class MuleClassTanker(Drone):

    @staticmethod
    def get_drone_type():
        return 'Probe Drone'

    @staticmethod
    def _get_default_inventory():
        return BasicInventory()

    def get_default_fuel_per_distance(self):
        return 1

    def get_default_distance_per_tick(self):
        return 0.5

    def _load_file_specifics(self, game_file):
        pass
