""" Container for ConsoleOutputHandler
"""
from scripts.interfaces.output_handler.output_handler import OutputHandler


class ConsoleOutputHandler(OutputHandler):

    def __init__(self):
        pass

    def welcome(self):
        print('Welcome to Shardnova!\n'
              'Type any command to continue.')

    def on_course(self, fuel_use, drone_fuel, destination, distance, ticks_to_finished):
        print('On course to: {0}\n'
              'Journey will consume {1}/{2} fuel to travel {3} pu.\n'
              'ETA: {4}'
              .format(destination, fuel_use, drone_fuel, distance, ticks_to_finished))

    def insufficient_fuel(self, destination, fuel_use, drone_fuel):
        print('Insufficient fuel to reach {0}.\n'
              'Journey requires {1} fuel with only {2} available.'
              .format(destination, fuel_use, drone_fuel))

    def check_course(self, destination, distance, ticks_to_finished, drone_fuel):
        print('On course to: {0}\n'
              'Fuel remaining: {1}\n'
              'Distance remaining: {2}\n'
              'ETA: {3}'
              .format(destination, drone_fuel, distance, ticks_to_finished))

    def no_course(self):
        print('No directive set.')

    def show_on_course_map(self, galaxy, sector, system, source, destination):
        message = self.__get_basic_map(galaxy, sector, system)
        message += 'On course from {0} to {1}'.format(source, destination)
        print(message)

    @staticmethod
    def __get_basic_map(galaxy, sector, system):
        message = ('Galaxy: {0}\n'
                   'Sector: {1}\n'
                   'System: {2}\n'
                   'Destinations within system:\n').format(galaxy, sector, system)
        for index, celestial_body in enumerate(system.get_celestial_bodies()):
            message += '{0}: {1}\n'.format(index, celestial_body)
        return message

    def show_map(self, galaxy, sector, system, celestial_body):
        message = self.__get_basic_map(galaxy, sector, system)
        message += 'Currently orbiting {0}'.format(celestial_body)
        print(message)

    def invalid_command(self):
        print('Invalid command')

    def invalid_index(self, index):
        print('Invalid index')
