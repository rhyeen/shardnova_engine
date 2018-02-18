""" Container for <I> Inventory
"""
from abc import ABC, abstractmethod
from scripts.classes.item.item_identifier import ItemIdentifier


class Inventory(ABC):

    def __init__(self):
        self._slots = []
        self.__max_slots = self._get_default_max_slots()
        self.__reset_slots()

    @staticmethod
    @abstractmethod
    def _get_default_max_slots():
        return 0

    def get_max_slots(self):
        return self.__max_slots

    def get_slots(self):
        return self._slots

    def __reset_slots(self):
        self._slots = [None] * self.__max_slots

    def add_item(self, item, slot=None):
        if slot is None:
            self.__fill_next_empty_slot(item)
        self.__fill_slot(item, slot)

    def __fill_next_empty_slot(self, item):
        slot = self.__get_empty_slot()
        if slot is None:
            raise ValueError('No more slots available to fill.')
        self._slots[slot] = item

    def __get_empty_slot(self):
        for index, slot in enumerate(self._slots):
            if slot is None:
                return index
        return None

    def __fill_slot(self, item, slot):
        if self.__slot_out_of_bounds(slot):
            raise ValueError('Slot {0} is out of range of inventory with max size of {1}.'
                             .format(slot, self.__max_slots))
        if self._slots[slot] is not None:
            raise ValueError('Slot {0} is already filled.'.format(slot))
        self._slots[slot] = item

    def __slot_out_of_bounds(self, slot):
        return slot < 0 or slot > self.__max_slots - 1

    def empty_slot(self, slot):
        if self.__slot_out_of_bounds():
            return
        self.__max_slots[slot] = None

    def get_all_items(self):
        return filter(lambda x: x is not None, self._slots)

    def load_file(self, game_file):
        self._load_file_generics(game_file)
        self._load_file_specifics(game_file)

    def _load_file_generics(self, game_file):
        self.__max_slots = game_file['maxSlots']
        for slot in game_file['slots']:
            item = ItemIdentifier.get_item_from_file(slot)
            self.add_item(item)

    @abstractmethod
    def _load_file_specifics(self, game_file):
        raise NotImplementedError
