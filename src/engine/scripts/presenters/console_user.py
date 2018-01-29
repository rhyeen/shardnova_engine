""" Container for ConsoleUser
"""
from scripts.interfaces.output_handler.console_output_handler import ConsoleOutputHandler


class ConsoleUser(object):

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

    def start_console(self):
        text = None
        while text != 'STOP':
            text = input('Next Command:')
            command = self.__get_command(text)
            self.__handle_input_command(command)

    def __get_command(self, text):
        text = self.__conform_text(text)
        if (text[0] == 'get map'):
            return ['GET', 'MAP']
        if (text[0] == 'set course'):
            command = ['SET', 'COURSE']
            command.push(int(text[1]))
            return command
        if (text[0] == 'check course'):
            return ['GET', 'COURSE']
        return ['INVALID']


    @staticmethod
    def __conform_text(text):
        commands = text.split(',')
        for index, command in enumerate(commands):
            commands[index] = command.strip().lower()
        return commands


    def __handle_input_command(self, command):
        if command[0] == 'INVALID':
            self.__user.output_handler.invalid_command()
            return
        if command[0] == 'GET':
            if command[1] == 'MAP':
                self.__interactor.get_map(self.__user, self.__drone)
            elif command[1] == 'COURSE':
                self.__interactor.check_course(self.__user, self.__drone)
        elif command[0] == 'SET':
            if command[1] == 'COURSE':
                self.__interactor.set_course(self.__user, self.__drone, command[2])
