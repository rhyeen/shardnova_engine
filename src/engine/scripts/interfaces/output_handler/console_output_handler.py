""" Container for ConsoleOutputHandler
"""
from scripts.interfaces.output_handler.output_handler import OutputHandler


class ConsoleOutputHandler(OutputHandler):

    def __init__(self):
        pass

    def welcome(self):
        print('Welcome to Shardnova!\n'
              'Type any command to continue.')

    def on_course(self, fuel_use, drone_fuel, distance_to_destination, ticks_to_finished):
        pass

    def insufficient_fuel(self, fuel_use, drone_fuel):
        pass

    def check_course(self, distance_to_destination, ticks_to_finished, drone_fuel):
        pass

    def no_course(self):
        pass

