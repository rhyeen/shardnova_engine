""" Container for ScriptedUser
"""

import time
from scripts.interfaces.output_handler.console_output_handler import ConsoleOutputHandler


class ScriptedUser(object):

    def __init__(self, interactor, user=None):
        self.__interactor = interactor
        if user is not None:
            user.output_handler = ConsoleOutputHandler()
            # Still need to ensure we bind the user to the interactor
            interactor.create_phone_user(user.get_primary_phone(), ConsoleOutputHandler())
        else:
            user = interactor.create_phone_user('+0', ConsoleOutputHandler())
        self.__user = user
        self.__drone = user.character.get_primary_drone()

    def basic_commands(self, kill_switch):
        # self.get_map(kill_switch)
        # self.check_course(kill_switch)
        self.set_course(kill_switch, 0)
        while True:
            self.check_course(kill_switch)
            time.sleep(5)

    def get_map(self, kill_switch):
        if kill_switch.should_kill():
            return
        self.__interactor.get_map(self.__user, self.__drone)

    def check_course(self, kill_switch):
        if kill_switch.should_kill():
            return
        self.__interactor.check_course(self.__user, self.__drone)

    def set_course(self, kill_switch, celestial_body_index):
        if kill_switch.should_kill():
            return
        self.__interactor.set_course(self.__user, self.__drone, celestial_body_index)
