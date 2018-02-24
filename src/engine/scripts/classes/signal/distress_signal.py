""" Container for DistressSignal
"""
from scripts.classes.signal.signal import Signal


class DistressSignal(Signal):

    def __init__(self, data_handler, drone):
        self._request = None
        self._distress_response_offers = {}
        self._accepted_distress_response_offer = None
        super().__init__(data_handler, drone)

    @staticmethod
    def get_signal_type():
        return 'Distress Signal'

    def set_request(self, request):
        self._request = request

    def get_request(self):
        return self._request

    def add_distress_response_offer(self, distress_response_offer):
        self._distress_response_offers[distress_response_offer.get_id()] = distress_response_offer

    def remove_distress_response_offer(self, distress_response_offer):
        self._distress_response_offers.pop(distress_response_offer.get_id(), None)

    def accept_distress_response_offer(self, distress_response_offer):
        self._drop_all_other_offers(distress_response_offer)
        self._accept_distress_response_offer(distress_response_offer)
        self._accepted_distress_response_offer = distress_response_offer

    def reject_distress_response_offer(self, distress_response_offer):
        key = distress_response_offer.get_id()
        if key not in self._distress_response_offers:
            raise ValueError('{0} not an offer for request {1}'.format(distress_response_offer, self))
        self._distress_response_offers[key].reject()


    def _drop_all_other_offers(self, distress_response_offer):
        for key in self._distress_response_offers:
            if key == distress_response_offer.get_id():
                continue
            self._distress_response_offers.drop()

    def _accept_distress_response_offer(self, distress_response_offer):
        key = distress_response_offer.get_id()
        if key not in self._distress_response_offers:
            raise ValueError('{0} not an offer for request {1}'.format(distress_response_offer, self))
        self._distress_response_offers[distress_response_offer.get_id()].accept()
