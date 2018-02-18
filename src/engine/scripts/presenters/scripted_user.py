""" Container for ScriptedUser
"""

import time
from scripts.kill_switch import KillSwitch


class ScriptedUser(object):

    def __init__(self, interactor, user, kill_switch=None):
        self.__interactor = interactor
        self.__user = user
        self.__drone = user.character.get_primary_drone()
        if kill_switch is None:
            kill_switch = KillSwitch()
        self.__kill_switch = kill_switch

    def basic_commands(self):
        # self.get_map()
        # self.check_course()
        self.set_course(0)
        while True:
            self.check_course()
            time.sleep(5)

    def get_command_function(self, command_function_name):
        return getattr(self, command_function_name)

    def get_map(self):
        if self.__kill_switch.should_kill():
            return
        self.__interactor.get_map(self.__user, self.__drone)

    def check_course(self):
        if self.__kill_switch.should_kill():
            return
        self.__interactor.check_course(self.__user, self.__drone)

    def set_course(self, celestial_body_index):
        if self.__kill_switch.should_kill():
            return
        self.__interactor.set_course(self.__user, self.__drone, celestial_body_index)
