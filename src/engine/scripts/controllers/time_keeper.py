""" Container for TimeKeeper
"""


class TimeKeeper(object):

    def __init__(self, game):
        """ game must come preloaded
        """
        self.__game = game

    def tick(self):
        self.__game.tick()
