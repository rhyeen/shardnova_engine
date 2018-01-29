""" Container for <I> DataHandler
"""
from abc import ABC, abstractmethod


class DataHandler(ABC):

    @abstractmethod
    def get_unique_id(self, id_type):
        return None

    @abstractmethod
    def get_unique_name(self, name_type):
        return None
