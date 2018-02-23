""" Container for ConsoleOutputHandler
"""
from scripts.interfaces.output_handler.output_handler import OutputHandler


class ConsoleOutputHandler(OutputHandler):

    def __init__(self, test_config=None):
        self.test_config = test_config
        self.output_records = {}

    def __report(self, report_id, report):
        self.output_records[report_id] = report

    def clear_records(self):
        self.output_records = {}

    def reached_destination(self, drone, course):
        report = {
            'drone': drone,
            'course': course
        }
        self.__report('reached_destination', report)

    def distress_signal_recieved(self, distress_signal):
        report = {
            'distress_signal': distress_signal
        }
        self.__report('distress_signal_recieved', report)

    def distress_signal_offer_received(self, distress_signal_offer):
        report = {
            'distress_signal_offer': distress_signal_offer
        }
        self.__report('distress_signal_offer_received', report)

    def distress_signal_offer_accepted(self, distress_signal):
        report = {
            'distress_signal': distress_signal
        }
        self.__report('distress_signal_offer_accepted', report)

    def distress_signal_offer_rejected(self, distress_signal):
        report = {
            'distress_signal': distress_signal
        }
        self.__report('distress_signal_offer_rejected', report)

    def distress_signal_dropped(self, distress_signal):
        report = {
            'distress_signal': distress_signal
        }
        self.__report('distress_signal_dropped', report)
