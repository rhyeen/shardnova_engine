""" Container for Offer
"""
from scripts.classes.exchange.exchange import Exchange


class Offer(Exchange):

    def __str__(self):
        return 'Offer:\n{0}'.format(self.get_exchange_details('max'))