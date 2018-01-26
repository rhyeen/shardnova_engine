""" Container for BasicInventory
"""
from scripts.classes.inventory.inventory import Inventory


class BasicInventory(Inventory):

    def _get_default_max_slots():
        return 4
