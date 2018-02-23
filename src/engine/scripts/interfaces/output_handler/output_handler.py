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

    @abstractmethod
    def distress_signal_sending(self, distress_signal):
        message = ('Sending distress signal {0} with request: {1}'
                   .format(distress_signal, distress_signal.get_request()))
        self.__report(message)

    @abstractmethod
    def distress_signal_recieved(self, distress_signal):
        pass

    @abstractmethod
    def distress_signal_offer_sending(self, distress_signal_offer):
        pass

    @abstractmethod
    def distress_signal_offer_received(self, distress_signal_offer):
        pass

    @abstractmethod
    def distress_signal_offer_accepted(self, distress_signal):
        pass

    @abstractmethod
    def distress_signal_offer_rejected(self, distress_signal):
        pass

    @abstractmethod
    def distress_signal_dropped(self, distress_signal):
        pass

    @abstractmethod
    def accepting_distress_signal_offer(self, distress_signal_offer):
        pass

    @abstractmethod
    def rejecting_distress_signal_offer(self, distress_signal_offer):
        pass
