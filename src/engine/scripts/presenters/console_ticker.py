""" Container for ConsoleTicker
"""


class ConsoleTicker(object):

    def __init__(self, time_keeper):
        self.__time_keeper = time_keeper

    def __tick(self):
        self.__time_keeper.tick()

    def start_console(self):
        text = None
        while text != 'STOP':
            text = input('Move time forward')
            self.__tick()
