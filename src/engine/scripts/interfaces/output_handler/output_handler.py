""" Container for <I> OutputHandler
"""
from abc import ABC, abstractmethod


class OutputHandler(ABC):

    @staticmethod
    @abstractmethod
    def send_welcome_message(user):
        return None
