""" Container for ConsoleOutputHandler
"""
import math
from scripts.interfaces.output_handler.output_handler import OutputHandler


class ConsoleOutputHandler(OutputHandler):

    def __init__(self, test_config=None):
        self.test_config = test_config
        self.output_records = []

    def __report(self, message):
        if self.test_config:
            if self.test_config.get('preserve_output', False):
                self.output_records.append(message)
            if self.test_config.get('silence_output', False):
                return
        print(message + '\n')

    def welcome(self):
        self.__report('Welcome to Shardnova!\n'
                      'Type any command to continue.')

    def on_course(self, fuel_use, drone_fuel, destination, distance, ticks_to_finished):
        self.__report('On course to: {0}\n'
                      'Journey will consume {1:0.1f}/{2:0.1f} fuel to travel {3:0.1f} pu.\n'
                      'ETA: {4} ticks'
                      .format(destination, fuel_use, drone_fuel, distance, math.ceil(ticks_to_finished)))

    def insufficient_fuel(self, destination, fuel_use, drone_fuel):
        self.__report('Insufficient fuel to reach {0}.\n'
                      'Journey requires {1:0.1f} fuel with only {2:0.1f} available.'
                      .format(destination, fuel_use, drone_fuel))

    def check_course(self, destination, distance, ticks_to_finished, drone_fuel):
        self.__report('On course to: {0}\n'
                      'Fuel remaining: {1:0.1f}\n'
                      'Distance remaining: {2:0.1f} pu\n'
                      'ETA: {3} ticks'
                      .format(destination, drone_fuel, distance, math.ceil(ticks_to_finished)))

    def no_course(self):
        self.__report('No directive set.')

    def show_on_course_map(self, galaxy, sector, system, source, destination):
        message = self.__get_basic_map(galaxy, sector, system)
        message += 'On course from {0} to {1}'.format(source, destination)
        self.__report(message)

    @staticmethod
    def __get_basic_map(galaxy, sector, system):
        message = ('{0}\n'
                   '{1}\n'
                   '{2}\n'
                   'Destinations within system:\n').format(galaxy, sector, system)
        for index, celestial_body in enumerate(system.get_celestial_bodies()):
            message += '{0}: {1}\n'.format(index, celestial_body)
        return message

    def show_map(self, galaxy, sector, system, celestial_body):
        message = self.__get_basic_map(galaxy, sector, system)
        message += 'Currently orbiting {0}'.format(celestial_body)
        self.__report(message)

    def invalid_command(self):
        self.__report('Invalid command')

    def invalid_index(self, index):
        self.__report('Invalid index')
