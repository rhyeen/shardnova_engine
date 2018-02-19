""" Container for SmsCredits
"""


class SmsCredits(object):

    def __init__(self):
        self.__max_credits = self.__get_default_max_credits()
        self.__remaining_credits = None
        self.reset_credits()

    @staticmethod
    def __get_default_max_credits():
        return 200

    def reset_credits(self):
        self.__remaining_credits = self.__max_credits

    def get_max_credits(self):
        return self.__max_credits

    def set_max_credits(self, credits):
        self.__max_credits = credits

    def get_remaining_credits(self):
        return self.__remaining_credits

    def use_credits(self, amount=1):
        self.__remaining_credits -= amount
        if self.__remaining_credits < 0:
            self.__remaining_credits = 0
            raise ValueError('No credits remain')

    def load_file(self, game_file):
        self.__max_credits = game_file['maxCredits']
        self.__remaining_credits = game_file['remainingCredits']
