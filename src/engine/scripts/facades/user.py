""" Container for User
"""
from scripts.facades.account_details import AccountDetails
from scripts.classes.character.player_character import PlayerCharacter


class User(object):

    def __init__(self):
        self.__account_details = AccountDetails()
        self.__character = PlayerCharacter()
