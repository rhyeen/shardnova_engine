""" Container for Npcs
"""
from scripts.classes.character.npc import Npc


class Npcs(object):

    def __init__(self, data_handler):
        self.__data_handler = data_handler
        self.__npcs = []

    def get_npcs(self):
        return self.__npcs

    def add_npc(self, npc):
        if self.__npc_exists(npc):
            return False
        self.__add_npc(npc)
        return True

    def __npc_exists(self, npc):
        return self.__get_npc_index(npc) is not None

    def __get_npc_index(self, npc):
        for index, __npc in enumerate(self.__npcs):
            if __npc.get_id() == npc.get_id():
                return index
        return None

    def __add_npc(self, npc):
        self.__npcs.append(npc)

    def remove_npc(self, npc):
        if not self.__npc_exists(npc):
            raise ValueError('{0} is not found.'.format(npc))
        index = self.__get_npc_index(npc)
        self.__remove_npc(index)

    def __remove_npc(self, npc_index):
        del self.__npcs[npc_index]

    def tick(self):
        for npc in self.__npcs:
            npc.tick()

    def make_choices(self):
        for npc in self.__npcs:
            npc.make_choices()

    def load_file(self, game_file, universe):
        for npc_file in game_file:
            npc = Npc(self.__data_handler, None)
            npc.load_file(npc_file, universe)
            self.add_npc(npc)
