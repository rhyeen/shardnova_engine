""" Container for RandomStringTestHandler
"""
import random
import string
from scripts.interfaces.data_handler.data_handler import DataHandler


class RandomStringTestHandler(DataHandler):

    def get_unique_id(self, id_type):
        return self._generate_id()

    def get_unique_name(self, name_type):
        return self._generate_id()

    @staticmethod
    def _generate_id():
        alphanumeric_choices = string.ascii_lowercase + string.ascii_uppercase + string.digits
        return ''.join(random.choice(alphanumeric_choices) for _ in range(6))
