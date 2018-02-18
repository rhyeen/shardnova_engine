""" Container for KillSwitch
"""


class KillSwitch(object):

    def __init__(self):
        self.__should_kill = False

    def should_kill(self):
        return self.__should_kill

    def flip_to_kill(self):
        self.__should_kill = True
