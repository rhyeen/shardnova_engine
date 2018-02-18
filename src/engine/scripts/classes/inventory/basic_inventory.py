""" Container for BasicInventory
"""
from scripts.classes.inventory.inventory import Inventory


class BasicInventory(Inventory):

    @staticmethod
    def _get_default_max_slots():
        return 4

    def _load_file_specifics(self, game_file):
        pass
