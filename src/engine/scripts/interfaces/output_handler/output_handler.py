""" Container for <I> OutputHandler
"""
from abc import ABC, abstractmethod


class OutputHandler(ABC):

    @abstractmethod
    def welcome(self):
        pass

    @abstractmethod
    def on_course(self, fuel_use, drone_fuel, destination, distance, ticks_to_finished):
        pass

    @abstractmethod
    def already_at_course_desintation(self, destination):
        pass

    @abstractmethod
    def insufficient_fuel(self, destination, fuel_use, drone_fuel):
        pass

    @abstractmethod
    def check_course(self, destination, distance, ticks_to_finished, drone_fuel):
        pass

    @abstractmethod
    def no_course(self):
        pass

    @abstractmethod
    def show_on_course_map(self, galaxy, sector, system, source, destination):
        pass

    @abstractmethod
    def show_map(self, galaxy, sector, system, celestial_body):
        pass

    @abstractmethod
    def invalid_command(self):
        pass

    @abstractmethod
    def invalid_index(self, index):
        pass

    @abstractmethod
    def reached_destination(self, drone, course):
        pass
