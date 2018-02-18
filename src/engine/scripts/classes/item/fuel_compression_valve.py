""" Container for FuelCompressionValve
"""
from scripts.classes.item.item import Item


class FuelCompressionValve(Item):

    def modifies_fuel_per_distance(self):
        return self._alter_by_durability(0.8)

    @staticmethod
    def _get_max_durability():
        return 10

    @staticmethod
    def _get_cost_per_repair_point():
        return 1

    def _load_file_specifics(self, game_file):
        pass
