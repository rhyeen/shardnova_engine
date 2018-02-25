""" Container for Offer
"""
from scripts.classes.exchange.exchange import Exchange


class Request(Exchange):

    def __str__(self):
        return 'Request:\n{0}'.format(self.get_exchange_details('min'))
