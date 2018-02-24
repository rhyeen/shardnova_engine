""" Container for DistressResponseOffer
"""
from scripts.classes.signal.signal import Signal


class DistressResponseOffer(Signal):

    def __init__(self, data_handler, drone, distress_signal):
        self._offer = None
        self.accepted = False
        self.rejected = False
        self.droppped = False
        self.distress_signal = distress_signal
        super().__init__(data_handler, drone)

    @staticmethod
    def get_signal_type():
        return 'Distress Response Offer'

    def set_offer(self, offer):
        self._offer = offer

    def get_offer(self):
        return self._offer

    def accept(self):
        self.accepted = True
        self.rejected = False
        self.droppped = False

    def reject(self):
        self.accepted = False
        self.rejected = True
        self.droppped = False

    def drop(self):
        self.accepted = False
        self.rejected = False
        self.droppped = True
