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
        self.__report('On course to {0}\n'
                      'Journey will consume {1:0.1f}/{2:0.1f} fuel to travel {3:0.1f} pu.\n'
                      'ETA: {4} ticks'
                      .format(destination, fuel_use, drone_fuel, distance, math.ceil(ticks_to_finished)))

    def already_at_course_desintation(self, destination):
        self.__report('Set destination is within no burn range.\n'
                      'Orbiting {0} now.'.format(destination))

    def insufficient_fuel(self, destination, fuel_use, drone_fuel):
        self.__report('Insufficient fuel to reach {0}.\n'
                      'Journey requires {1:0.1f} fuel with only {2:0.1f} available.'
                      .format(destination, fuel_use, drone_fuel))

    def check_course(self, destination, distance, ticks_to_finished, drone_fuel):
        self.__report('On course to {0}\n'
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

    def reached_destination(self, drone, course):
        self.__report('{0} reached {1}'.format(drone, course.get_destination()))

    def distress_signal_sending(self, distress_signal):
        message = ('Distress signal {0} sent with request: {1}'
                   .format(distress_signal, distress_signal.get_request()))
        self.__report(message)

    def distress_signal_recieved(self, distress_signal):
        message = ('Distress signal {0} sent from {1} {2} {3}'
                   .format(distress_signal, distress_signal.galaxy, distress_signal.sector, distress_signal.sector))
        message += 'Sent by {0}'.format(distress_signal.get_drone_type())
        message += 'Request: {0}'.format(distress_signal.get_request())
        self.__report(message)

    def distress_signal_offer_sending(self, distress_signal_offer):
        message = 'Distress signal {0} responded to with offer: {1}'.format(distress_signal_offer.distress_signal, distress_signal_offer)
        self.__report(message)

    def distress_signal_offer_received(self, distress_signal_offer):
        message = ('Distress response {0} sent from {1} {2} {3}'
                   .format(distress_signal_offer.get_offer(), distress_signal_offer.galaxy, distress_signal_offer.sector, distress_signal_offer.sector))
        message += 'Sent by {0}'.format(distress_signal_offer.get_drone_type())
        message += 'Offer: {0}'.format(distress_signal_offer)
        self.__report(message)

    def distress_signal_offer_accepted(self, distress_signal):
        self.__report('Offer for distress signal {0} was accepted.'.format(distress_signal))

    def distress_signal_offer_rejected(self, distress_signal):
        self.__report('Offer for distress signal {0} was rejected.'.format(distress_signal))

    def distress_signal_dropped(self, distress_signal):
        self.__report('Distress signal {0} dropped.'.format(distress_signal))

    def accepting_distress_signal_offer(self, distress_signal_offer):
        self.__report('Accepted distress signal offer {0}'.format(distress_signal_offer))

    def rejecting_distress_signal_offer(self, distress_signal_offer):
        self.__report('Rejecting distress signal offer {0}'.format(distress_signal_offer))
