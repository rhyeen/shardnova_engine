""" Container for FactionReputs
"""


class FactionReputs(object):

    def __init__(self):
        self.__faction_map = {}

    def add_faction(self, faction):
        factionName = faction.get_name()
        if factionName in self.__faction_map:
            raise ValueError('{0} already has a reput'.format(faction))
        self.__faction_map[factionName] = self.__get_default_faction_object(faction)

    def __get_default_faction_object(faction):
        return {
            'faction': faction,
            'reputation': None
        }

    def get_faction(self, factionName):
        if (factionName not in self.__faction_map):
            return None
        return self.__faction_map[factionName]['faction']

    def get_faction_reputation(self, factionName):
        if (factionName not in self.__faction_map):
            return None
        return self.__faction_map[factionName]['reputation']
