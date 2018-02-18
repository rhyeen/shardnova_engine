""" Container for FactionReputs
"""
from scripts.classes.universal_faction import UniversalFaction


class FactionReputs(object):

    def __init__(self):
        self.__faction_map = {}

    def add_faction(self, faction, reputation=None):
        faction_name = faction.get_name()
        if faction_name in self.__faction_map:
            raise ValueError('{0} already has a reput'.format(faction))
        self.__faction_map[faction_name] = self.__get_faction_object(faction, reputation)

    def __get_faction_object(faction, reputation=None):
        return {
            'faction': faction,
            'reputation': reputation
        }

    def get_faction(self, faction_name):
        if (faction_name not in self.__faction_map):
            return None
        return self.__faction_map[faction_name]['faction']

    def get_faction_reputation(self, faction_name):
        if (faction_name not in self.__faction_map):
            return None
        return self.__faction_map[faction_name]['reputation']

    def load_file(self, game_file):
        for faction_file in game_file['factionMap']:
            faction_type = faction_file['faction']['type']
            if faction_type == 'universal':
                faction = UniversalFaction()
            else:
                raise ValueError('Faction of type "{0}" unsupported'.format(faction_type))
            faction.load_file(faction_file['faction'])
            self.add_faction(faction, faction_file['reputation'])
