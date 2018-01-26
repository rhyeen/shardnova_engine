""" Container for ProbeDrone
"""
from scripts.classes.drone.drone import Drone
from scripts.classes.inventory.basic_inventory import BasicInventory


class ProbeDrone(Drone):

    def _get_default_inventory():
        return BasicInventory()
