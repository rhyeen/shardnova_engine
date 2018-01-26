""" Container for <I> DataHandler
"""
from abc import ABC, abstractmethod


class DataHandler(ABC):

    @staticmethod
    @abstractmethod
    def get_unique_id(id_type):
        return None
