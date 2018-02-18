""" Container for ItemIdentifier
"""
from scripts.classes.item.fuel_compression_valve import FuelCompressionValve


class ItemIdentifier(object):

    @staticmethod
    def get_item_from_file(game_file):
        if 'type' not in game_file:
            return None
        item_type = game_file['type']
        item_type_map = ItemIdentifier.__get_item_type_map()
        if item_type not in item_type_map:
            raise ValueError('Item of type "{0}" unsupported'.format(item_type))
        item = item_type_map[item_type]
        item.load_file(game_file)
        return item

    @staticmethod
    def __get_item_type_map():
        return {
            'fuelCompressionValve': FuelCompressionValve()
        }
